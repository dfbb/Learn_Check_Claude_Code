package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

type Question struct {
	ID          string            `yaml:"id" json:"id"`
	Difficulty  string            `yaml:"difficulty" json:"difficulty"`
	Question    string            `yaml:"question" json:"question"`
	Options     map[string]string `yaml:"options" json:"options"`
	Correct     string            `yaml:"correct" json:"correct"`
	Explanation string            `yaml:"explanation" json:"explanation"`
	Category    string            `yaml:"-" json:"category"`
}

type YAMLFile struct {
	Category   string     `yaml:"category"`
	CategoryID int        `yaml:"category_id"`
	Questions  []Question `yaml:"questions"`
}

var allQuestions []Question
var questionsDir string

func loadQuestions(dir string) ([]Question, error) {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return nil, err
	}
	var result []Question
	for _, e := range entries {
		if e.IsDir() || (!strings.HasSuffix(e.Name(), ".yaml") && !strings.HasSuffix(e.Name(), ".yml")) {
			continue
		}
		data, err := os.ReadFile(filepath.Join(dir, e.Name()))
		if err != nil {
			continue
		}
		var yf YAMLFile
		if err := yaml.Unmarshal(data, &yf); err != nil {
			continue
		}
		for i := range yf.Questions {
			yf.Questions[i].Category = yf.Category
		}
		result = append(result, yf.Questions...)
	}
	return result, nil
}

func filterByDifficulty(questions []Question, difficulty string, count int) []Question {
	var filtered []Question
	for _, q := range questions {
		if q.Difficulty == difficulty {
			filtered = append(filtered, q)
		}
	}
	rand.Shuffle(len(filtered), func(i, j int) { filtered[i], filtered[j] = filtered[j], filtered[i] })
	if len(filtered) > count {
		filtered = filtered[:count]
	}
	return filtered
}

func difficultyCount(d string) int {
	switch d {
	case "junior":
		return 20
	case "senior":
		return 30
	case "power":
		return 30
	}
	return 20
}

func difficultyLabel(d string) string {
	switch d {
	case "junior":
		return "初级"
	case "senior":
		return "中级"
	case "power":
		return "高级"
	}
	return d
}

func appendResult(text string) error {
	f, err := os.OpenFile("result.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer f.Close()
	_, err = f.WriteString(text)
	return err
}

func handleQuestions(w http.ResponseWriter, r *http.Request) {
	difficulty := r.URL.Query().Get("difficulty")
	if difficulty == "" {
		http.Error(w, "missing difficulty", http.StatusBadRequest)
		return
	}
	count := difficultyCount(difficulty)
	questions := filterByDifficulty(allQuestions, difficulty, count)
	if len(questions) == 0 {
		http.Error(w, "no questions for this difficulty", http.StatusBadRequest)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(questions)
}

type SubmitRequest struct {
	Name       string   `json:"name"`
	Difficulty string   `json:"difficulty"`
	Answers    []string `json:"answers"` // user answers indexed by question order
	Questions  []struct {
		ID          string            `json:"id"`
		Question    string            `json:"question"`
		Options     map[string]string `json:"options"`
		Correct     string            `json:"correct"`
		Explanation string            `json:"explanation"`
	} `json:"questions"`
	ElapsedSeconds int `json:"elapsed_seconds"`
}

func handleSubmit(w http.ResponseWriter, r *http.Request) {
	var req SubmitRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}
	if req.Name == "" || req.Difficulty == "" {
		http.Error(w, "missing name or difficulty", http.StatusBadRequest)
		return
	}

	total := len(req.Questions)
	correct := 0
	var lines []string
	for i, q := range req.Questions {
		userAns := ""
		if i < len(req.Answers) {
			userAns = req.Answers[i]
		}
		isCorrect := strings.EqualFold(userAns, q.Correct)
		if isCorrect {
			correct++
			lines = append(lines, fmt.Sprintf("%s [正确] %s", q.ID, q.Question))
		} else {
			lines = append(lines, fmt.Sprintf("%s [错误] 你的答案: %s | 正确答案: %s | %s", q.ID, userAns, q.Correct, q.Question))
		}
	}

	mins := req.ElapsedSeconds / 60
	secs := req.ElapsedSeconds % 60
	pct := 0
	if total > 0 {
		pct = correct * 100 / total
	}

	record := fmt.Sprintf(
		"=====================================\n姓名：%s\n难度：%s\n完成时间：%s\n用时：%d分%d秒\n得分：%d/%d (%d%%)\n-------------------------------------\n%s\n=====================================\n\n",
		req.Name,
		difficultyLabel(req.Difficulty),
		time.Now().Format("2006-01-02 15:04:05"),
		mins, secs,
		correct, total, pct,
		strings.Join(lines, "\n"),
	)

	if err := appendResult(record); err != nil {
		http.Error(w, "failed to write result", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]any{
		"correct": correct,
		"total":   total,
		"percent": pct,
	})
}

type AbandonRequest struct {
	Name       string `json:"name"`
	Difficulty string `json:"difficulty"`
	Answered   int    `json:"answered"`
	Total      int    `json:"total"`
}

func handleAbandon(w http.ResponseWriter, r *http.Request) {
	var req AbandonRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusOK)
		return
	}
	record := fmt.Sprintf(
		"=====================================\n姓名：%s\n难度：%s\n状态：未完成（已答 %d/%d 题）\n退出时间：%s\n=====================================\n\n",
		req.Name,
		difficultyLabel(req.Difficulty),
		req.Answered, req.Total,
		time.Now().Format("2006-01-02 15:04:05"),
	)
	appendResult(record)
	w.WriteHeader(http.StatusOK)
}

func main() {
	questionsDir = filepath.Join(".", "questions-zh")
	if _, err := os.Stat(questionsDir); os.IsNotExist(err) {
		questionsDir = filepath.Join("..", "questions-zh")
	}
	var err error
	allQuestions, err = loadQuestions(questionsDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to load questions: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Loaded %d questions\n", len(allQuestions))

	htmlDir := filepath.Join(questionsDir, "html")
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" {
			http.ServeFile(w, r, filepath.Join(htmlDir, "index.html"))
			return
		}
		http.NotFound(w, r)
	})
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir(htmlDir))))
	http.HandleFunc("/api/questions", handleQuestions)
	http.HandleFunc("/api/submit", handleSubmit)
	http.HandleFunc("/api/abandon", handleAbandon)

	fmt.Println("Server running at http://localhost:8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Fprintf(os.Stderr, "server error: %v\n", err)
		os.Exit(1)
	}
}

package api

import "fmt"

type TVshow struct {
	Id               string
	OriginCountry    string
	OriginalLanguage string
	PosterPath       string
	FirstAirDate     string
	Name             string
	Overview         string
	VoteAverage      int
	Cast             []string
}

func Hello() {
	fmt.Println("Hello, Api!")
}

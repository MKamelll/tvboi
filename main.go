package main

import (
	"fmt"
	"net/http"

	"github.com/a-h/templ"
	"github.com/mkamelll/tvboi/api"
	views "github.com/mkamelll/tvboi/resources/views"
)

func main() {
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))
	port := ":3000"
	http.Handle("/", templ.Handler(views.Dashboard("TVboi")))

	breaking_bad := api.TVshow{
		Name:       "Breaking Bad",
		Overview:   "A chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine with a former student to secure his family's future.",
		PosterPath: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOcWkpWG_NRrU2M8-WB8EbEcJk7smhdrY1eO0ttKXm0bo2ooOEWxk3zBSbsFrSgSJh2OEKOQ",
		Cast: []string{
			"Bryan Cranston", "Anna Gunn", "Aaron Paul", "Dean Norris", "Betsy Brandt", "RJ Mitte", "Giancarlo Esposito",
		},
	}

	http.Handle("/tvshow", templ.Handler(views.TVshow(breaking_bad)))

	fmt.Println("You're app is running on: http://localhost" + port)
	http.ListenAndServe(port, nil)
}

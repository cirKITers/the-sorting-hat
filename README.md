# The Sorting Hat

This is a small [Dash](https://dash.plotly.com/) app that aims to solve the problem of assigning topics (e.g. in context of a practical course) to students.
Considering a number of students and a fixed number seats for each available topic, the students can rate each topic on a scale from 1-5.
Depending on the rating and the number of available seats, the tool will then assign the topics accordingly and reports the overall satisfaction.

![Example](docs/TheSortingHatExample.png)

The solver uses [nevergrad](https://github.com/facebookresearch/nevergrad) for finding a solution.

## Getting started

Head to this [demo site](https://ef1622d3-5380-4dfa-a196-0931e40ee13a.ka.bw-cloud-instance.org/) for playing around or start locally:

1. Clone/ download
2. `poetry install`
3. `poetry run python app/app.py`

Everything else should be self-explainatory.
You can find hints by hovering the UI components and by clicking the "Help" button on the left sidepanel.

---

*Of course, this is not related to the "real" [Sorting Hat](https://harrypotter.fandom.com/wiki/Sorting_Hat)*
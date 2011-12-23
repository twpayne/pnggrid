all: tests summary

.PHONY: tests
tests:
	python tests.py

.PHONY: summary
summary: demo-summary europe-summary

.PHONY: demo-summary
demo-summary: demo.json demo.json.gz demo.png
	stat -c "%n: %s" demo.json demo.json.gz demo.png

demo.json.gz: demo.json
	gzip -9 -c $< > $@

demo.png: demo.json
	python utfgrid2pnggrid.py $<

.PHONY: europe-summary
europe-summary: europe.json europe.json.gz europe.png
	stat -c "%n: %s" europe.json europe.json.gz europe.png

europe.json.gz: europe.json
	gzip -9 -c $< > $@

europe.png: europe.json
	python utfgrid2pnggrid.py $<

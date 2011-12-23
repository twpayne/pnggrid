all: tests summary

.PHONY: tests
tests:
	python tests.py

.PHONY: summary
summary: demo-summary europe-summary

.PHONY: demo-summary
demo-summary: demo.json demo.json.gz demo.png demo.optipng.png
	stat -c "%n: %s" $^

demo.json.gz: demo.json
	gzip -9 -c $< > $@

demo.optipng.png: demo.png
	cp $< $@
	optipng -q -o7 $@

demo.png: demo.json
	python utfgrid2pnggrid.py $<

.PHONY: europe-summary
europe-summary: europe.json europe.json.gz europe.png europe.optipng.png
	stat -c "%n: %s" $^

europe.json.gz: europe.json
	gzip -9 -c $< > $@

europe.optipng.png: europe.png
	cp $< $@
	optipng -q -o7 $@

europe.png: europe.json
	python utfgrid2pnggrid.py $<

.PHONY: clean
clean:
	rm -f demo.json.gz demo.png europe.json.gz europe.png

MARP    := npx --yes @marp-team/marp-cli@4.5.1
DECK    := slides.md
THEME   := theme.css
FLAGS   := --no-stdin --theme-set $(THEME) --allow-local-files --html
export CHROME_PATH ?= /usr/bin/chromium-browser

.PHONY: preview pdf html pptx clean

preview:
	$(MARP) $(DECK) $(FLAGS) --preview

pdf html pptx:
	$(MARP) $(DECK) $(FLAGS) --$@ -o slides.$@

clean:
	rm -f slides.pdf slides.html slides.pptx

MARP    := npx --yes @marp-team/marp-cli@latest
DECK    := slides.md
THEME   := theme.css
FLAGS   := --theme-set $(THEME) --allow-local-files
export CHROME_PATH ?= /usr/bin/chromium-browser

.PHONY: preview pdf html pptx clean

preview:
	$(MARP) $(DECK) $(FLAGS) --preview

pdf html pptx:
	$(MARP) $(DECK) $(FLAGS) --$@ -o slides.$@

clean:
	rm -f slides.pdf slides.html slides.pptx

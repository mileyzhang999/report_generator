.PHONY: all a b c

all: a b c

a:
	@read -p "Enter input: " input; \
    echo "Input: $$input"; \
    echo "$$input" > input.txt; \
	python fetchapi.py "$$input"

b:
	python script.py

c:
	@input=$$(cat input.txt); \
    echo "Input: $$input"; \
	python pushapi.py "$$input"


clean:
	@echo "Deleting all the markdown and pdf files ..."
	@rm -f *.md
	@rm -f *.pdf
	@rm -f *.txt
	@rm -f *.html
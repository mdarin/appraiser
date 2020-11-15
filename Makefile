QUADRATIC = quadratic
LINEAR = linear
QUASILINEAR = quasilinear

all: $(QUADRATIC) $(LINEAR) $(QUASILINEAR) estimations

build: $(QUADRATIC) $(LINEAR) $(QUASILINEAR)

estimations:
	@./run.sh


## quadratic

$(QUADRATIC): $(QUADRATIC).o
	@gcc  -o $(QUADRATIC) $(QUADRATIC).o
	@echo 'compiled program: $(QUADRATIC)'

$(QUADRATIC).o: $(QUADRATIC).c
	@gcc -c -Wall $(QUADRATIC).c
     
clean_$(QUADRATIC):
	-rm $(QUADRATIC).o $(QUADRATIC)

## linear

$(LINEAR): $(LINEAR).o
	@gcc -o $(LINEAR) $(LINEAR).o
	@echo 'compiled program: $(LINEAR)'

$(LINEAR).o: $(LINEAR).c
	@gcc -c -Wall $(LINEAR).c
     
clean_$(LINEAR):
	-rm $(LINEAR).o $(LINEAR)

## quasilinear

$(QUASILINEAR): $(QUASILINEAR).o
	@gcc -o $(QUASILINEAR) $(QUASILINEAR).o
	@echo 'compiled program: $(QUASILINEAR)'

$(QUASILINEAR).o: $(QUASILINEAR).c
	@gcc -c $(QUASILINEAR).c
     
clean_$(QUASILINEAR):
	-rm $(QUASILINEAR).o $(QUASILINEAR)

clean: clean_$(QUASILINEAR) clean_$(LINEAR) clean_$(QUADRATIC)
	@echo 'cleaned up'

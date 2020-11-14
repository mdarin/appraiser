QUADRATIC = quadratic
LINEAR = linear
QUASILINEAR = quasilinear

all: $(QUADRATIC) $(LINEAR) $(QUASILINEAR)

## quadratic

$(QUADRATIC): $(QUADRATIC).o
	@gcc  -o $(QUADRATIC) $(QUADRATIC).o

$(QUADRATIC).o: $(QUADRATIC).c
	@gcc -c -Wall $(QUADRATIC).c
     
clean_$(QUADRATIC):
	@rm $(QUADRATIC).o $(QUADRATIC)

## linear

$(LINEAR): $(LINEAR).o
	@gcc -o $(LINEAR) $(LINEAR).o

$(LINEAR).o: $(LINEAR).c
	@gcc -c -Wall $(LINEAR).c
     
clean_$(LINEAR):
	@rm $(LINEAR).o $(LINEAR)

## quasilinear

$(QUASILINEAR): $(QUASILINEAR).o
	@gcc -o $(QUASILINEAR) $(QUASILINEAR).o

$(QUASILINEAR).o: $(QUASILINEAR).c
	@gcc -c $(QUASILINEAR).c
     
clean_$(QUASILINEAR):
	@rm $(QUASILINEAR).o $(QUASILINEAR)


clean:
	@echo 'cleaned up'
	@rm *.o 
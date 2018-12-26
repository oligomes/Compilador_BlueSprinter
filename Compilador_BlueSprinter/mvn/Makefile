JAVA=/usr/bin/java

# Diretórios
SRCDIR=src
BINDIR=assembler
LIBDIR=biblioteca
BIB_ARQS = boolean const environment comparacao push_pop heap

# montador MVN
MONTADOR=montador.MvnAsm
LINKADOR=linker.MvnLinker
RELOCADOR=relocator.MvnRelocator

.PRECIOUS: %.mvn

vpath %.asm $(SRCDIR):$(LIBDIR)

%.mvn: %.asm
	$(JAVA) -cp $(BINDIR)/MLR.jar $(MONTADOR) $^
	rm $*.lst

%: $(SRCDIR)/%.mvn $(addprefix $(LIBDIR)/, $(addsuffix .mvn, $(BIB_ARQS)))
	$(JAVA) -cp $(BINDIR)/MLR.jar $(LINKADOR) $^ -s $(BINDIR)/linkado.mvn
	$(JAVA) -cp $(BINDIR)/MLR.jar $(RELOCADOR) $(BINDIR)/linkado.mvn $(BINDIR)/saida.mvn 0000 0000
	if [ ! -e $(saida).mvn ] ;\
		then ln -s $(BINDIR)/$(saida).mvn . ;\
	fi;
	rm $(BINDIR)/linkado.mvn
	rm $(saida).run
	rm $<

run:
	@$(JAVA) -jar $(BINDIR)/mvn.jar

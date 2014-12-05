CC=gcc
LD=gcc
RM=rm -f
VERBOSE=@
CFLAGS=-g3 -O0 -Wall -Werror -D_LARGEFILE_SUPPORT -D_FILE_OFFSET_BITS=64
INCPATH=-Isrc/

.PHONY: all
all: mpegrecover ;

src/analysis.o: src/analysis.c src/analysis.h src/dllist.h src/mpeg.h
	@echo [CC] src/analysis.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

src/mpeg.o: src/mpeg.c src/endianness.h src/mpeg.h
	@echo [CC] src/mpeg.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

src/endianness.o: src/endianness.c src/endianness.h
	@echo [CC] src/endianness.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

src/dllist.o: src/dllist.c src/dllist.h
	@echo [CC] src/dllist.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

src/buffer.o: src/buffer.c src/buffer.h
	@echo [CC] src/buffer.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

src/main.o: src/main.c src/analysis.h src/dllist.h src/buffer.h \
 src/endianness.h src/mpeg.h
	@echo [CC] src/main.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

tests/analysis.o: tests/analysis.c src/analysis.h src/dllist.h \
 src/dllist.h src/endianness.h src/mpeg.h
	@echo [CC] tests/analysis.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

tests/mpeg.o: tests/mpeg.c src/endianness.h src/mpeg.h
	@echo [CC] tests/mpeg.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

tests/dllist.o: tests/dllist.c src/dllist.h
	@echo [CC] tests/dllist.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

tests/buffer.o: tests/buffer.c src/buffer.h
	@echo [CC] tests/buffer.o
	${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<

tests/analysis: tests/analysis.o src/analysis.o src/dllist.o src/endianness.o src/mpeg.o
	@echo [LD] tests/analysis
	${VERBOSE}${LD} ${CFLAGS} -o $@ $^

tests/buffer: tests/buffer.o src/buffer.o
	@echo [LD] tests/buffer
	${VERBOSE}${LD} ${CFLAGS} -o $@ $^

tests/dllist: tests/dllist.o src/dllist.o
	@echo [LD] tests/dllist
	${VERBOSE}${LD} ${CFLAGS} -o $@ $^

tests/mpeg: tests/mpeg.o src/mpeg.o src/endianness.o
	@echo [LD] tests/mpeg
	${VERBOSE}${LD} ${CFLAGS} -o $@ $^

mpegrecover: src/main.o src/analysis.o src/buffer.o src/dllist.o src/endianness.o src/mpeg.o
	@echo [LD] mpegrecover
	${VERBOSE}${LD} ${CFLAGS} -o $@ $^

.PHONY: tests
tests: tests/analysis tests/buffer tests/dllist tests/mpeg ;
.PHONY: clean
clean:
	${RM} src/analysis.o src/mpeg.o src/endianness.o src/dllist.o src/buffer.o src/main.o tests/analysis.o tests/mpeg.o tests/dllist.o tests/buffer.o
	${RM} tests/analysis tests/buffer tests/dllist tests/mpeg mpegrecover

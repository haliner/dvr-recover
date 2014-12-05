# Binaries to use
JAVAC   = javac
JAVADOC = javadoc
JAR     = jar
CP      = cp


# Some target name variables
RELEASE_JAR = mpegrecover.jar
RELEASE_ENTRY_POINT = mpegrecover.MpegRecover

TESTS_JAR = mpegrecover-tests.jar
TESTS_ENTRY_POINT = mpegrecover.tests.MpegRecoverTest

JAVADOC_DIR = javadoc/


# All public classes that are needed for a release.
# The public classes are in there own files, but their *.java file might
# build other (private) classes, too.
RELEASE_CLASSES = \
	mpegrecover/configuration/Configuration.class \
	mpegrecover/configuration/ConfigurationException.class \
	mpegrecover/core/MpegRecover.class \
	mpegrecover/core/MpegRecoverException.class \
	mpegrecover/mpeg/MpegBlock.class \
	mpegrecover/mpeg/MpegFragment.class \
	mpegrecover/mpeg/MpegTimestamp.class

# All public classes that are needed for testing.
# The public classes are in there own files, but their *.java file might
# build other (private) classes, too.
TEST_CLASSES = \
	mpegrecover/tests/ConfigurationTest.class \
	mpegrecover/tests/MpegRecoverTest.class \
	mpegrecover/tests/MpegTimestampTest.class

# All private classes that are needed for testing.
# Private classes don't have their own *.java file, but will be build by
# another *.java file automatically in the build process.
TEST_CLASSES_PRIVATE = \
	mpegrecover/tests/MpegTimestampTestable.class


.PHONY: all
all: ${RELEASE_JAR} ;


.PHONY: clean
clean:
	rm -f ${RELEASE_CLASSES} ${TEST_CLASSES} ${TEST_CLASSES_PRIVATE} ${RELEASE_JAR} ${TESTS_JAR}
	rm -rf ${JAVADOC_DIR}


.PHONY: tests
tests: ${TESTS_JAR} ;


.PHONY: javadoc
javadoc:
	${JAVADOC} -private -d ${JAVADOC_DIR} -subpackages mpegrecover


%.class: %.java
	${JAVAC} $^


mpegrecover.jar: ${RELEASE_CLASSES}
	${JAR} -cfe ${RELEASE_JAR} ${RELEASE_ENTRY_POINT} ${RELEASE_CLASSES}


mpegrecover-tests.jar: ${RELEASE_CLASSES} ${TEST_CLASSES}
	${JAR} -cfe ${TESTS_JAR} ${TESTS_ENTRY_POINT} ${RELEASE_CLASSES} ${TEST_CLASSES} ${TEST_CLASSES_PRIVATE}


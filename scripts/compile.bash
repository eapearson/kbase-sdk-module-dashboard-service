if [ "${DEV}" = "true" ] 
then
    echo "In Dev mode, not generating report (DEV=${DEV})"
else
    echo "Not in Dev mode, will generate compilation report (DEV=${DEV})"
    export KB_SDK_COMPILE_REPORT_FILE=./work/compile_report.json
fi

export SERVICE_CAPS=$1
export SPEC_FILE=$2
export LIB_DIR=$3

echo "Compiling with: ${SERVICE_CAPS}, ${SPEC_FILE}, ${LIB_DIR}"

kb-sdk compile ${SPEC_FILE} \
		--out ${LIB_DIR} \
		--plclname ${SERVICE_CAPS}::${SERVICE_CAPS}Client \
		--jsclname javascript/Client \
		--pyclname ${SERVICE_CAPS}.${SERVICE_CAPS}Client \
		--javasrc src \
		--java \
		--pysrvname ${SERVICE_CAPS}.${SERVICE_CAPS}Server \
		--pyimplname ${SERVICE_CAPS}.${SERVICE_CAPS}Impl;
#!/bin/bash
set -x

USAGE="
Usage:
    update-swagger-ui.sh -v <SWAGGER_UI_VERSION>
    update-swagger-ui.sh -h (or --help)
"

version=""

while getopts "v:h" arg
do
    case $arg in
        v) version=$2; shift 2;;
        h) echo "${USAGE}"; exit 0;;
        ?) echo "args error: $1"; exit 1;;
    esac
done

echo ${version}

archive="https://github.com/swagger-api/swagger-ui/archive/v${version}.tar.gz"

folder="swagger-ui-${version}"
rm -rf "${folder}" && mkdir -p "${folder}"
wget $archive -O - | tar -xvz -C "$folder" --strip-components=1

# folder="swagger-ui-3.19.3"
rm -rf ./static/* ./templates/*

rsync -rzvaP ${folder}/LICENSE ./swagger_ui/static/
rsync -rzvaP ${folder}/LICENSE ./swagger_ui/templates/

rsync -rzvaP ${folder}/dist/*.html ./swagger_ui/templates/
rsync -rzvaP ${folder}/dist/* --exclude *.html ./swagger_ui/static/

sed -i 's#<title>.*</title>#<title> {{ title }} </title>#g' ./swagger_ui/templates/index.html
sed -i 's#src="\.#src="{{ url_prefix }}#g' ./swagger_ui/templates/index.html
sed -i 's#href="\.#href="{{ url_prefix }}#g' ./swagger_ui/templates/index.html
sed -i 's#https://petstore.swagger.io/v[1-9]#{{ url_prefix }}#g' ./swagger_ui/templates/index.html
sed -i 's#layout: "StandaloneLayout"#defaultModelsExpandDepth: 0, validatorUrl: null, layout: "BaseLayout"#g' ./swagger_ui/templates/index.html

rm -fr "$folder"

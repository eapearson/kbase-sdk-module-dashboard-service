# Local Development with kbase-ui

## Setup this module

clone this repo, kb_sdk, and kbase-ui

```
mkdir project
cd project
git clone https://github.com/kbase/kb_sdk
git clone https://github.com/kbase/kbase-sdk-module-dashboard-service
git clone https://github.com/kbase/kbase-ui
```

build kb_sdk

> note, you just use java 8 and also have ant installed

```
cd kb_sdk
make
```

build dashboard image

```
cd ../kbase-sdk-module-dashboard-service
make
make docker-image-dev
```

start the dashboard image

```
make test
```

this will generate some local directories.

> oops, need to create this:

```
mkdir -p test_local/workdir/cache
```

start the service locally

```
make run-docker-image-dev
```


## kbase-ui

```
cd ../kbase-ui
make dev-start env=dev build=dev build-image=t dynamic-services="DashboardService"
```

## Edit /etc/hosts

Edit /etc/hosts to add this line

```
127.0.0.1       ci.kbase.us
```

You should be good to go on https://ci.kbase.us



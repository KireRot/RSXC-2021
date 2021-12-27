# Day 18 - Remember the flag? Docker remembers

We found a docker image, but it seems that the flag has been removed from it, could you help us get it back?

## Write-Up
Today we are facing a challenge involving a docker image. We start by downloading the file and unzip it. The files we get are *Dockerfile* and *docker-box.tar.gz*. Let's extract the *docker-box.tar.gz* before we dig into this.

At first it seems that extracting the *docker-box.tar* does not do anything, but comparing the filesize it reveals that it containd a new tar file with the same name. Continue to extract and we will get output similar to this.

```shell
$ tar -xvf ./docker-box.tar
docker-box.tar

$ tar -xvf ./docker-box.tar
277cb1d569ea184dace14bf1fe3b107122fa64472087074df1b617d8e8fac40c.json
4d91099b6eba4c0dcb124fd368532a2aad219aaed4245e3f57e56467fd4ea947/
4d91099b6eba4c0dcb124fd368532a2aad219aaed4245e3f57e56467fd4ea947/VERSION
4d91099b6eba4c0dcb124fd368532a2aad219aaed4245e3f57e56467fd4ea947/json
4d91099b6eba4c0dcb124fd368532a2aad219aaed4245e3f57e56467fd4ea947/layer.tar
5dee72d2797c533813effb8e9de26377300d29f418ebb06bfe814f950a7aa02b/
5dee72d2797c533813effb8e9de26377300d29f418ebb06bfe814f950a7aa02b/VERSION
5dee72d2797c533813effb8e9de26377300d29f418ebb06bfe814f950a7aa02b/json
5dee72d2797c533813effb8e9de26377300d29f418ebb06bfe814f950a7aa02b/layer.tar
9fe4b6808af55b1cba8de0e09b728d09f52480307744bed28e164167426f03b8/
9fe4b6808af55b1cba8de0e09b728d09f52480307744bed28e164167426f03b8/VERSION
9fe4b6808af55b1cba8de0e09b728d09f52480307744bed28e164167426f03b8/json
9fe4b6808af55b1cba8de0e09b728d09f52480307744bed28e164167426f03b8/layer.tar
manifest.json
repositories
```

From the output we see that we have some files called *layer.tar*, *json* and *VERSION* in three different directories. We'll make a not of this for later. The [Docker Docs](https://docs.docker.com/storage/storagedriver/) can give us some information about docker images and layers.

*"A Docker image is built up from a series of layers. Each layer represents an instruction in the image’s Dockerfile. Each layer except the very last one is read-only."*

Let us look at our *Dockerfile*

```shell
$ cat Dockerfile                   
FROM alpine:3.14
COPY ./flag.txt /flag.txt
RUN rm /flag.txt
```

Using the information from *Docker Docs* we see that this *Dockerfile* contains three commands. Commands that modify the filesystem create a layer. The `FROM` statement starts out by creating a layer from the `alpine:3.14` image. The `COPY` command adds some files from the Docker client’s current directory. The first, and only, `RUN` command builds the application using the `make` command, and writes the result to a new layer.

Looking at the contents in the *manifest.json* file we can find information about the layers.
```
$ cat manifest.json | jq | cat -n
 1	[
 2	  {
 3	    "Config": "277cb1d569ea184dace14bf1fe3b107122fa64472087074df1b617d8e8fac40c.json",
 4	    "RepoTags": [
 5	      "docker-box:latest"
 6	    ],
 7	    "Layers": [
 8	      "5dee72d2797c533813effb8e9de26377300d29f418ebb06bfe814f950a7aa02b/layer.tar",
 9	      "9fe4b6808af55b1cba8de0e09b728d09f52480307744bed28e164167426f03b8/layer.tar",
10	      "4d91099b6eba4c0dcb124fd368532a2aad219aaed4245e3f57e56467fd4ea947/layer.tar"
11	    ]
12	  }
13	]
```

As we have figured out, we have three layers. Each created by the commands in *Dockerfile*. The first layer is only containing the *alpine:3.14* data and are not what we are lookging for. In the second layer, the flag.txt should exist as it is added to the image at this point. The third layer will be "Too Late" as the flag file is deleted here. From *line 9* above, we see where the second layer is located. Let us extract this layer and see if we find our flag.

```shell
$ tar -xvf ./9fe4b6808af55b1cba8de0e09b728d09f52480307744bed28e164167426f03b8/layer.tar 
flag.txt

$ cat flag.txt
RSXC{Now_you_know_that_docker_images_are_like_onions.They_have_many_layers}
```

## The Flag
RSXC{Now_you_know_that_docker_images_are_like_onions.They_have_many_layers}
docker buildx build --output=type=image,push=true,format=docker --platform linux/arm/v7 -t zeroprg/ultralitics:arm32v7 .
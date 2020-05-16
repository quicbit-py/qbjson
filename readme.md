# qb-json-next

A python 2 implementation of [qb-json-next](https://github.com/quicbit-js/qb-json-next). Please refer to
that documentation for more detail.

While this is the same logic as the nodejs version, the nodejs version is super-quick at ~300 MB per second
and C version is about 1 GB per second! 

while this parser has unremarkable performance of 2 MB per second - pretty standard unoptimized processing speed.

There is nothing terribly amiss with the python implementation and performance is probably in line
with other python parsers (?). Feedback on how this tokenizer can be made fast in python is welcome.

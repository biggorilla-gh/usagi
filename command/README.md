exec:

```
./run command/cli.py
```

## quit
finish process.

```
>> quit
```

## total
Displays the total number of documents.

example:

```
>>  total
total: 8
```

## search 
Search the document.

```
search <keyword>
```

example:

```
>>  search Product
hits: 3
<ClassicModels.public.Products>   Products   ClassicModels/public
<ClassicModels.public.ProductLines>   ProductLines   ClassicModels/public
<ClassicModels.public.OrderDetails>   OrderDetails   ClassicModels/public
```

## filters
Display a list of filters.

```
filter <depth>
```

example:

```
>>  filters
1:ClassicModels

>>  filters 2
1:ClassicModels
   2:public
```
# JSON format of for loop.

<pre>
> use sat
switched to db sat
> show collections
definition
looptype
system.indexes
> db.looptype.find()
{ "_id" : ObjectId("58819df0b7dfe71ee2366846"), "type" : "type3", "linenumber" : 95, "location" : "libxl.c" }
</pre>

<pre>
void libxl_string_list_destroy(libxl_string_list *psl)
{
    int i;
    libxl_string_list sl = *psl;

    if (!sl)
        return;

    for (i = 0; sl[i] != NULL; i++)
        free(sl[i]);
    free(sl);
}
</pre>

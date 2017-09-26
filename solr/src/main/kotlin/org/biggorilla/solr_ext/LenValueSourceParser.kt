package org.biggorilla.solr_ext

import org.apache.lucene.index.LeafReaderContext
import org.apache.lucene.queries.function.FunctionValues
import org.apache.lucene.queries.function.ValueSource
import org.apache.lucene.queries.function.docvalues.LongDocValues
import org.apache.solr.search.FunctionQParser
import org.apache.solr.search.ValueSourceParser

/**
 * Created by toshiyuki on 2016/12/22.
 */
class LenValueSourceParser : ValueSourceParser() {

    override fun parse(fp: FunctionQParser?): ValueSource? {
        return LenValueSource(fp!!.parseArg())
    }

    class LenValueSource(val field: String) : ValueSource() {

        override fun hashCode(): Int {
            return javaClass.hashCode() + field.hashCode()
        }

        override fun equals(other: Any?): Boolean {
            other ?: return false
            if (javaClass != other.javaClass) return false
            return field.equals((other as LenValueSource).field)
        }

        override fun getValues(context: MutableMap<Any?, Any?>?, readerContext: LeafReaderContext?): FunctionValues? {
            return object : LongDocValues(this) {
                override fun longVal(doc: Int): Long {
                    readerContext ?: return 0
                    val r = readerContext.reader()
                    val tv = r.getTermVector(doc, field)
                    if (tv == null) return 0
                    return tv.size()
                }
            }
        }

        override fun description(): String? {
            return "len($field)"
        }
    }
}

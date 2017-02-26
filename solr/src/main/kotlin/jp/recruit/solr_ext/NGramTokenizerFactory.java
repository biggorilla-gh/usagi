package jp.recruit.solr_ext;

import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.ngram.NGramTokenizer;
import org.apache.lucene.analysis.util.TokenizerFactory;
import org.apache.lucene.util.AttributeFactory;

import java.io.Reader;
import java.util.Map;

public class NGramTokenizerFactory extends TokenizerFactory {
    private final int maxGramSize;
    private final int minGramSize;

    /**
     * Creates a new NGramTokenizerFactory
     */
    public NGramTokenizerFactory(Map<String, String> args) {
        super(args);
        minGramSize = getInt(args, "minGramSize", NGramTokenizer.DEFAULT_MIN_NGRAM_SIZE);
        maxGramSize = getInt(args, "maxGramSize", NGramTokenizer.DEFAULT_MAX_NGRAM_SIZE);
        if (!args.isEmpty()) {
            throw new IllegalArgumentException("Unknown parameters: " + args);
        }
    }

    /**
     * Creates the {@link TokenStream} of n-grams from the given {@link Reader} and {@link AttributeFactory}.
     */
    @Override
    public Tokenizer create(AttributeFactory factory) {
        return new NGramTokenizer(factory, minGramSize, maxGramSize);
    }
}


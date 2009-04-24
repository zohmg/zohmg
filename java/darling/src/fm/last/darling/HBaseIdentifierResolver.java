package fm.last.darling;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.streaming.io.IdentifierResolver;
import org.apache.hadoop.streaming.io.TextInputWriter;
import org.apache.hadoop.streaming.io.TypedBytesInputWriter;
import org.apache.hadoop.streaming.io.TypedBytesOutputReader;

/**
 * By setting <tt>stream.io.identifier.resolver.class=HBaseIdentifierResolver</tt>
 * and giving the option <tt>-outputformat table</tt> to dumbo
 * you will be able to store stuff in HBase.
 * 
 * Pro-tip: Remember to set <tt>hbase.mapred.outputtable</tt>.
 *
 */
public class HBaseIdentifierResolver extends IdentifierResolver {
	public static final String HBASE_ID = "hbase";

	/**
	 * Tries to resolve a given identifier, falls back on super class.
	 */
	public void resolve(String identifier) {
		if (identifier.equalsIgnoreCase(HBASE_ID)) {
			System.err.println("HBaseIdentifierResolver.resolve: HBASE.\n");
			setInputWriterClass(TextInputWriter.class);
			setOutputReaderClass(HBaseOutputReader.class);
			setOutputKeyClass(ImmutableBytesWritable.class);
			setOutputValueClass(BatchUpdate.class);
		} else {
			super.resolve(identifier);
		}
	}
}


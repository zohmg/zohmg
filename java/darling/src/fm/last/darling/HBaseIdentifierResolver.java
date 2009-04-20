package fm.last.darling;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.hbase.io.BatchUpdate;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.streaming.io.IdentifierResolver;
import org.apache.hadoop.streaming.io.TextInputWriter;
import org.apache.hadoop.streaming.io.TypedBytesInputWriter;
import org.apache.hadoop.streaming.io.TypedBytesOutputReader;

/**
 * By pointing <tt>stream.io.identifier.resolver.class</tt> to this class
 * and giving the option <tt>-outputformat table</tt> to dumbo
 * you will be able to store stuff in HBase.
 * 
 * Pro-tip: Remember to set <tt>hbase.mapred.outputtable</tt>.
 *
 */
public class HBaseIdentifierResolver extends IdentifierResolver {
	public static final String HBASE_ID = "hbase";
	public static final String LOLWHAT_ID = "lolwhat";

	/**
	 * Resolves a given identifier, falls back on super class.
	 */
	public void resolve(String identifier) {
		System.err.println("HBaseIdentifierResolver");
		if (identifier.equalsIgnoreCase(HBASE_ID)) {
			System.err.println("HBaseIdentifierResolver.resolve: DOING HBASE.\n");
			setInputWriterClass(TextInputWriter.class); // do I really want to spec. this?
			setOutputReaderClass(HBaseOutputReader.class);
			setOutputKeyClass(ImmutableBytesWritable.class);
			setOutputValueClass(BatchUpdate.class);
		} else if (identifier.equalsIgnoreCase(LOLWHAT_ID)) {
			System.err.println("HBaseIdentifierResolver.resolve: DOING TableOutputWriter?\n");
			setInputWriterClass(TextInputWriter.class);
			setOutputReaderClass(HBaseOutputReader.class);
			setOutputKeyClass(ImmutableBytesWritable.class);
			setOutputValueClass(BatchUpdate.class);
		} else {
			super.resolve(identifier);
		}
	}
}


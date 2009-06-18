package fm.last.darling.hbase;

import java.io.IOException;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.HTable;


// write a single row to hbase.
public class BasicPut {
	
	public void write_row(String tablename, String rowkey, String family, String qualifier, String value) throws IOException {
		HTable table = new HTable(tablename);
		Put p = new Put(rowkey.getBytes());
		p.add(family.getBytes(), qualifier.getBytes(), value.getBytes());
		table.put(p);
	}

	public static void main(String[] args) {
		System.out.println("what bizarre shit.");
		
		String table = "stuff";
		String rowkey = "user-1001-track-200-20090616";
		String family = "unit";
		String qualifier = "scrobbles";
		String scrobbles = "16";
		
		BasicPut bp = new BasicPut();
		try {
			bp.write_row(table, rowkey, family, qualifier, scrobbles);
		} catch (IOException e) {
			System.err.println("oh noes.");
		}
	}
}

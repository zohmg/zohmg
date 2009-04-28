package fm.last.darling.hbase;

import fm.last.darling.utils.Util;

public class HBaseUtils {
	// totally non-customizable rowkey formatter.
	public static byte[] formatRowkey(String unit, long epoch) {
        String ymd = Util.EpochtoYMD(epoch);
        String rowkey = unit + "-" + ymd;
        return rowkey.getBytes();
	}
}

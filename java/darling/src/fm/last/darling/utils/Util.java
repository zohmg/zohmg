package fm.last.darling.utils;

import java.util.Calendar;
import java.util.GregorianCalendar;

public class Util {
	public static String EpochtoYMD(long epoch) {
        Calendar thence = new GregorianCalendar();
        thence.setTimeInMillis(epoch*1000);
        int year = thence.get(Calendar.YEAR);
        int month = thence.get(Calendar.MONTH) + 1;
        int day = thence.get(Calendar.DAY_OF_MONTH);
        return String.format("%04d%02d%02d", year, month, day);
	}

	// TODO: this is not used no more. remove at will. 
	// the following was lifted from http://forums.sun.com/thread.jspa?threadID=609364
	/**
	 * Returns a byte array containing the two's-complement representation of the integer.<br>
	 * The byte array will be in big-endian byte-order with a fixes length of 4
	 * (the least significant byte is in the 4th element).<br>
	 * <br>
	 * <b>Example:</b><br>
	 * <code>intToByteArray(258)</code> will return { 0, 0, 1, 2 },<br>
	 * <code>BigInteger.valueOf(258).toByteArray()</code> returns { 1, 2 }. 
	 * @param integer The integer to be converted.
	 * @return The byte array of length 4.
	 */
	public static byte[] intToByteArray (final int integer) {
		int byteNum = (40 - Integer.numberOfLeadingZeros (integer < 0 ? ~integer : integer)) / 8;
		byte[] byteArray = new byte[4];

		for (int n = 0; n < byteNum; n++)
			byteArray[3 - n] = (byte) (integer >>> (n * 8));

		return (byteArray);
	}
	
	public static void main(String[] args) {
		System.out.println("yeah, utils.");
		System.out.println(Util.EpochtoYMD(1240300000)); // => Tue Apr 21 08:46:40 +0100 2009
		System.out.println(Util.EpochtoYMD(1210000000)); // => Mon May 05 16:06:40 +0100 2008
		System.out.println(Util.EpochtoYMD(123000));     // => Fri Jan 02 11:10:00 +0100 1970
	}
}

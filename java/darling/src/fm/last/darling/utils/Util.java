package fm.last.darling.utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;

import org.ho.yaml.Yaml;

import fm.last.darling.nspace.Dimension;

public class Util {
	
	public static String EpochtoYMD(long epoch) {
        Calendar thence = new GregorianCalendar();
        thence.setTimeInMillis(epoch*1000);
        int year = thence.get(Calendar.YEAR);
        int month = thence.get(Calendar.MONTH) + 1;
        int day = thence.get(Calendar.DAY_OF_MONTH);
        return String.format("%04d%02d%02d", year, month, day);
	}
	
	public static ArrayList<ArrayList<Dimension>> readRequestedProjections(File yaml) throws FileNotFoundException {

		// open file, read yaml, turn into pumpkin.
		try {
			Object object = Yaml.load(yaml);
		} catch {
			
		}
		
		ArrayList<ArrayList<Dimension>> expected = new ArrayList<ArrayList<Dimension>>();
		ArrayList<Dimension> projection0 = new ArrayList<Dimension>();
		projection0.add(new Dimension("country"));
		expected.add(projection0);
		ArrayList<Dimension> projection1 = new ArrayList<Dimension>();
		projection1.add(new Dimension("country"));
		projection1.add(new Dimension("service"));
		expected.add(projection1);		

		return expected;
	}
}

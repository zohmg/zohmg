package fm.last.darling.util;

import java.io.File;
import java.util.ArrayList;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

import fm.last.darling.nspace.Dimension;
import fm.last.darling.utils.Util;

public class UtilTest {

	@Test
	public void testEpochtoYMD() {
		String expected = "20090421";
		String ymd = Util.EpochtoYMD(1240300000);
		assertEquals(ymd, expected);
	}
	
	@Test
	public void testreadRequestedProjections() {
		File testDataFolder = new File("test/data"); 
		File yaml = new File(testDataFolder, "dataset.yaml");
		ArrayList<ArrayList<Dimension>> ret = Util.readRequestedProjections(yaml);
		
		ArrayList<ArrayList<Dimension>> expected = new ArrayList<ArrayList<Dimension>>();
		ArrayList<Dimension> projection0 = new ArrayList<Dimension>();
		projection0.add(new Dimension("country"));
		expected.add(projection0);
		ArrayList<Dimension> projection1 = new ArrayList<Dimension>();
		projection1.add(new Dimension("country"));
		projection1.add(new Dimension("service"));
		expected.add(projection1);		
		
		
		assertEquals(ret.size(), expected.size());
		for (int i = 0; i < ret.size(); i++)
			assertEquals(ret.get(i).toString(), expected.get(i).toString());
	}
	
	
}

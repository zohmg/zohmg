package fm.last.darling.mapred;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;
import java.util.TreeMap;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import fm.last.darling.io.records.NSpacePoint;
import fm.last.darling.nspace.Dimension;
import fm.last.darling.nspace.Projectionist;
import fm.last.darling.user.UserMapper;

// the class we wrap around the user's mapper.
public class MapperWrapper implements Mapper<LongWritable, Text, NSpacePoint, IntWritable> {
	private UserMapper usermapper;

	public MapperWrapper() throws Exception {
		// TODO: read name of user's mapper class from config.
		String userclass = "fm.last.darling.user.ExampleMapper";

		// dynamically instantiate user's mapper class.
		try {
			usermapper = (UserMapper) Class.forName(userclass).newInstance();
		} catch(Exception e) {
			System.err.println("could not instantiate userclass " + userclass + ": " + e.toString());
			throw new IOException("instantiation fail.");
		}
	}
	
	public void close() throws IOException {}
	public void configure(JobConf conf) {}

	// wrap this map around the user's mapper.
	public void map(LongWritable key, Text value, OutputCollector<NSpacePoint, IntWritable> collector, Reporter reporter) throws IOException {
		// call on user's mapper
		ZohmgOutputCollector o = new ZohmgOutputCollector();
		usermapper.map(key.get(), value.toString(), o);
		long ts = o.getTimestamp();
		TreeMap<String,String> points = o.getDimensions();
		
		// fan out into projections,
		ArrayList<ArrayList<Dimension>> rps = readRequestedProjections();
		for (ArrayList<Dimension> requested : rps) {
			// reduce down to the dimensions we are interested in. 
			TreeMap<String,String> projection = Projectionist.dimensionality_reduction(requested, points);
			// emit once for every unit.
			for (String unit : o.measurementUnits()) {
				NSpacePoint point = new NSpacePoint(ts, projection, unit);
				collector.collect(point, o.getMeasurement(unit));
			}
        }
	}

	private ArrayList<ArrayList<Dimension>> readRequestedProjections() {
		ArrayList<ArrayList<Dimension>> list = new ArrayList<ArrayList<Dimension>>();

		ArrayList<Dimension> projection0 = new ArrayList<Dimension>();
		projection0.add(new Dimension("country"));
		list.add(projection0);

		ArrayList<Dimension> projection1 = new ArrayList<Dimension>();
		projection1.add(new Dimension("country"));
		projection1.add(new Dimension("service"));
		list.add(projection1);

		return list;
	}
	
	// TODO: not used for anything else than illustrative purposes. remove at will.
	public static void main(String[] args) throws Exception {
		System.out.println("yeah, that's right.");

		// proof of concept.
		ZohmgOutputCollector o = new ZohmgOutputCollector();
		String userclass = "fm.last.darling.user.ExampleMapper";
		UserMapper usermapper = (UserMapper) Class.forName(userclass).newInstance();
		usermapper.map(200, "123423423	SE	web	510", o);
	}
}

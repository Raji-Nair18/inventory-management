public class MainActivity extends AppCompatActivity {
 @Override
 protected void onCreate(Bundle b){
  super.onCreate(b);
  WebView w=new WebView(this);
  w.getSettings().setJavaScriptEnabled(true);
  w.loadUrl("http://10.0.2.2:5000");
  setContentView(w);
 }
}

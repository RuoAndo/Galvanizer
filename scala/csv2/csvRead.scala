import scala.io.Source
import java.io.PrintWriter

object csvRead {

  def address_format(line : String, out : PrintWriter) = {
    val list = line split ','
    
    val zip = dropQuote(list(0))    
    val address = dropQuote(list(2)) // + dropQuote(list(3))
    print("%s,%s\n" format (zip, address))
    out.write("%s,%s\n" format (zip, address))
  }

  // 前後のダブルクォーテーションを除去
  def dropQuote(str : String) : String = {
    str drop 1 dropRight 1
  }

  def main(args: Array[String]): Unit = {
    println("Reading " + args(0))
    // 入力ファイル
    val source = Source.fromFile(args(0), "ms932")
    // 出力ファイル   
    val out = new PrintWriter("zip_and_address.txt", "utf8")
    // ファイルを読み込んでループ
    val lines = source.getLines
    lines.foreach(line => address_format(line, out))
    source.close
    out.close
  }
}
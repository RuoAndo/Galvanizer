import akka.actor._
import scala.collection.mutable.ListBuffer

/*
case class MapCompleted()
case class ReduceCompleted()
*/

class MapActor extends Actor {

  import context._

  val mapOutputs = new ListBuffer[MapOutput]
  val reduceInputs = new ListBuffer[ReduceInput]
  val reduceOutputs = new ListBuffer[ReduceOutput]

  // メッセージハンドラとなるメソッド
  def receive = {
    case s: String =>
    	    println("mapActor: %s".format(s))
	    val words = new ListBuffer[(String, Int)]
  	    s.split(' ').foreach(words += _->1)
            println("List :" + words)
            stop(self)
    // case _ => println("unknown")
  }
}
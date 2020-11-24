import akka.actor._
import scala.collection.mutable.ListBuffer

case class MapOutput(val entries:List[(String, Int)])
case class ReduceInput(val key:String, val entries:List[(String, Int)])
case class ReduceOutput(val key:String, val value:Int)
case class Begin()

case class FirstMessage(prop1: List[String])

case class MapCompleted()
case class ReduceCompleted()

class MainActor extends Actor with ActorLogging {
  import context._

  val mapOutputs = new ListBuffer[MapOutput]
  val reduceInputs = new ListBuffer[ReduceInput]
  val reduceOutputs = new ListBuffer[ReduceOutput]

  val MapRef = system.actorOf(Props[MapActor], name = "MapActor")
  var dataLength = 0

  val ReduceRef = system.actorOf(Props[ReduceActor], name = "ReduceActor")

  def receive = {
    case FirstMessage(prop1) => map(0, prop1)
    	 dataLength = prop1.length
    case mo: MapOutput =>
    	 println("MapOutput received")
	 appendMapOutput(mo)
	 checkMapProgress
    case MapCompleted => println("Received: MapCompleted")
    	 println(sort(mapOutputs.toList))
         println(split(sort(mapOutputs.toList)))
	 reduce(0,split(sort(mapOutputs.toList)))
	 
    case _ => log.warning("unknown")
  }

  def map(index: Int, data:List[String]) {
    data match {
      case Nil =>
      case x::xs => println("Main calls map():" + x)
		    MapRef ! x
                    map(index+1, xs)
    }
  }

  def reduce(index: Int, data:List[ReduceInput]) {
    data match {
      case Nil =>
      case x::xs => ReduceRef ! x
                    reduce(index+1, xs)
    }
  }

  def sort(mapOutputs:List[MapOutput]) = {
    val words = new ListBuffer[(String, Int)]
    mapOutputs.foreach(words ++= _.entries)
    words.toList.sortWith(_._1 < _._1)
  }

  def split(data:List[(String, Int)]): List[ReduceInput] = {
    data match {
      case Nil => reduceInputs.toList
      case x::xs => {
        var spannedXs = xs.span(_._1 == x._1)
        reduceInputs += createReduceInput(x, spannedXs._1)
        split(spannedXs._2)
      }
    }
  }

  def createReduceInput(head: (String, Int),
                        remainder: List[(String, Int)]) = {
    val entries = new ListBuffer[(String, Int)] += head
    entries ++= remainder
    val reduceInput = ReduceInput(head._1, entries.toList)
    println("MasterActor: created: " + reduceInput)
    reduceInput
  }

  def appendMapOutput(o: MapOutput) = {
    println("MasterActor: received the response: map(" + o + ")")
    mapOutputs += o
    println("--->" + mapOutputs)
  }

  def checkMapProgress =
    if (mapOutputs.length == dataLength) MapRef ! MapCompleted
}

/**
 * Main
 */
object MapSample extends App {
  val system = ActorSystem()

  val data = List("Hello World",
                  "Hello Scala World",
                  "Hello Java World",
                  "Hello Java Hello",
                  "Hello Scala Scala",
                  "Scala World World World",
                  "Scala World Scala World",
                  "Hello Groovy")

  // アクターの生成
  val ref = system.actorOf(Props[MainActor], name = "mainActor")
  ref ! FirstMessage(data)

  Thread.sleep(3000)
  // println(mapOutputs)
  // すべてのアクターを終了
  system.terminate()
}
//package jp.sf.amateras.scala.akka

import akka.actor._

case class MapOutput(val entries:List[(String, Int)])
case class ReduceInput(val key:String, val entries:List[(String, Int)])
case class ReduceOutput(val key:String, val value:Int)
case class Begin()

/**
 * アクターを使った並行処理のサンプルです。
 */
class MainActor extends Actor with ActorLogging {
  import context._

  // 子のアクターを生成
  val subref = actorOf(Props[SubActor], name = "subActor")
  // 子のアクターの終了をモニタリング
  watch(subref)

  // メッセージハンドラとなるメソッド
  def receive = {
    case s: String => subref ! s		        // 子のアクターへ送信
    case Terminated(subref) => println("SubActor終了")	// 子のアクターの終了時
    case _ => log.warning("unknown")
  }
}

/**
 * メインのアクターから生成される子のアクターです。
 */
/*
class SubActor extends Actor {
  import context._

  def receive = {
    case s: String => println("メッセージ受信: %s".format(s))
      // 子のアクターを終了
      stop(self)
  }
}
*/

/**
 * Main
 */
object NormalActorSample extends App {
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

  // メッセージの送信
  ref ! "send message"

  Thread.sleep(3000)
  // すべてのアクターを終了
  system.terminate()
}
import akka.actor._

/**
 * メインのアクターから生成される子のアクターです。
 */
class SubActor extends Actor {
  import context._

  def receive = {
    case s: String => println("メッセージ受信: %s".format(s))
      // 子のアクターを終了
      stop(self)
  }
}


def p(&block)
  "<p>#{yield}</p>"
end

class Test

  def method_missing(meth, *arg, &block)
    puts "#{meth} called with #{arg.inspect}"
    super
  end

  def body
    p { # <text>stuff</text><div><image src='google link'/><text>caption</text></div>
      text 'stuff'
      div {
        image src="google link"
        text 'caption'
      }
    }
    p {
      text 'more text'
    }
  end

  def foo
    something
  end
end

Test.new.foo

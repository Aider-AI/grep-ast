import pytest

from tree_sitter_language_pack import get_parser

from grep_ast.dump import dump  # noqa: F401
from grep_ast.parsers import PARSERS

def test_get_parser_for_all_parsers():
    for lang in PARSERS.values():
        assert get_parser(lang) is not None

def assert_parses(language: str, source_code: str):
    """
    Assert that the given source code can be parsed by the specified language parser
    and that the resulting parse tree has a valid structure.
    """
    ext = next(ext for ext, lang in PARSERS.items() if lang == language)
    parser = get_parser(PARSERS[ext])
    tree = parser.parse(source_code.encode('utf-8'))

    assert tree is not None, f"Failed to parse {language} code"
    assert tree.root_node is not None, f"Parsed {language} tree has no root node"
    assert tree.root_node.child_count > 0, f"Parsed {language} tree has no children"

    errors = []
    def collect_errors(node, depth=0):
        if node.type == 'ERROR':
            errors.append(f"{'  ' * depth}Error at {node.start_point}: {node.text.decode('utf-8')}")
        for child in node.children:
            collect_errors(child, depth + 1)

    collect_errors(tree.root_node)

    assert not errors, f"Parsed {language} tree contains the following errors:\n" + "\n".join(errors)

    # Check that the tree has a reasonable depth
    def tree_depth(node):
        if not node.children:
            return 1
        return 1 + max(tree_depth(child) for child in node.children)

    assert tree_depth(tree.root_node) > 2, f"Parsed {language} tree has suspicious depth"

def test_parse_actionscript():
    assert_parses("actionscript", """
package {
    import flash.display.Sprite;

    public class Greeter extends Sprite {
        public function Greeter() {
            var message:String = "Hello, ActionScript!";
            trace(message);
        }
    }
}
""")

def test_parse_ada():
    assert_parses("ada", """
with Ada.Text_IO; use Ada.Text_IO;

procedure Hello is
begin
   Put_Line ("Hello, Ada!");
end Hello;
""")

def test_parse_ada_spec():
    assert_parses("ada", """
package Greetings is
   procedure Say_Hello (Name : in String);
end Greetings;
""")

def test_parse_agda():
    assert_parses("agda", """
module HelloAgda where

open import Agda.Builtin.IO
open import Agda.Builtin.Unit
open import Agda.Builtin.String

postulate
  putStrLn : String → IO ⊤

main : IO ⊤
main = putStrLn "Hello, Agda!"
""")

def test_parse_arduino():
    assert_parses("arduino", """
int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);
}
""")

def test_parse_asm():
    assert_parses("asm", """
        .section .text
        .globl _start
    _start:
        movl $1, %eax
        movl $0, %ebx
        int $0x80
    """)

def test_parse_astro():
    assert_parses("astro", """
---
const pageTitle = "Home Page";
---
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{pageTitle}</title>
  </head>
  <body>
    <h1>{pageTitle}</h1>
  </body>
</html>
    """)

def test_parse_bash():
    assert_parses("bash", """
#!/bin/bash
echo "Hello, World!"
for i in {1..5}
do
   echo "Number: $i"
done
    """)

def test_parse_beancount():
    assert_parses("beancount", """
2023-06-15 open Assets:Checking
2023-06-15 open Expenses:Food

2023-06-16 * "Grocery Store" "Weekly shopping"
  Assets:Checking  -50.00 USD
  Expenses:Food     50.00 USD
    """)

def test_parse_bibtex():
    assert_parses("bibtex", """
@article{einstein1905electrodynamics,
  title={On the electrodynamics of moving bodies},
  author={Einstein, Albert},
  journal={Annalen der Physik},
  volume={17},
  number={10},
  pages={891--921},
  year={1905},
  publisher={Wiley Online Library}
}
    """)

def test_parse_bicep():
    assert_parses("bicep", """
param location string = 'eastus'
param storageAccountName string = 'mystorageaccount'

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}
    """)

def test_parse_bitbake():
    assert_parses("bitbake", """
SUMMARY = "Simple example recipe"
DESCRIPTION = "This is a simple example recipe in BitBake"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://example.c"

do_compile() {
    ${CC} example.c -o example
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 example ${D}${bindir}
}
    """)

def test_parse_c():
    assert_parses("c", """
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
    """)

def test_parse_c_header():
    assert_parses("c", """
#ifndef EXAMPLE_H
#define EXAMPLE_H

#define MAX_SIZE 100

typedef struct {
    int id;
    char name[MAX_SIZE];
} Person;

void greet(Person *p);

#endif // EXAMPLE_H
    """)

def test_parse_cairo():
    assert_parses("cairo", """
func main() {
    let x = 5;
    let y = 3;
    let sum = x + y;
    return (sum);
}
""")

def test_parse_capnp():
    assert_parses("capnp", """
@0xE4A8D8C9A0B0C1E2;  # Unique file ID

struct Person {
  name @0 :Text;
  age @1 :UInt32;
  address @2 :Address;

  struct Address {
    street @0 :Text;
    city @1 :Text;
    country @2 :Text;
  }
}
""")

def test_parse_chatito():
    assert_parses("chatito", """
%[greet]('training': '1000', 'testing': '100')
    ~[hi] ~[name?]

~[hi]
    hey
    hello
    hi

~[name]
    Alice
    Bob
    Charlie
""")

def test_parse_clarity():
    assert_parses("clarity", """
(define-public (say-hi (name (string-ascii 50)))
  (ok (concat "Hello, " name "!"))
)

(say-hi "World")
""")

def test_parse_clojure():
    assert_parses("clojure", """
(ns hello-world.core)

(defn greet
  "A simple greeting function"
  [name]
  (str "Hello, " name "!"))

(println (greet "Clojure"))
""")

def test_parse_cmake():
    assert_parses("cmake", """
cmake_minimum_required(VERSION 3.10)

project(HelloWorld VERSION 1.0)

add_executable(hello_world main.cpp)

target_include_directories(hello_world PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
""")

def test_parse_commonlisp():
    assert_parses("commonlisp", """
(defun greet (name)
  "A simple greeting function"
  (format t "Hello, ~a!~%" name))

(greet "Common Lisp")
""")

def test_parse_cpon():
    assert_parses("cpon", """
{
  "name": "John Doe",
  "age": 30,
  "isStudent": false,
  "grades": [85, 90, 92],
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "country": "USA"
  }
}
""")

def test_parse_cpp():
    assert_parses("cpp", """
#include <iostream>
#include <string>

class Greeter {
public:
    static void greet(const std::string& name) {
        std::cout << "Hello, " << name << "!" << std::endl;
    }
};

int main() {
    Greeter::greet("C++");
    return 0;
}
""")

def test_parse_csharp():
    assert_parses("csharp", """
using System;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, C#!");
    }
}
""")

def test_parse_css():
    assert_parses("css", """
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
""")

def test_parse_csv():
    assert_parses("csv", """
Name,Age,City
John,30,New York
Alice,25,Los Angeles
Bob,35,Chicago
""")

def test_parse_cuda():
    assert_parses("cuda", """
__global__ void vectorAdd(float *a, float *b, float *c, int n)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    if (i < n)
        c[i] = a[i] + b[i];
}
""")

def test_parse_d():
    assert_parses("d", """
import std.stdio;

void main()
{
    writeln("Hello, D!");
}
""")

def test_parse_dart():
    assert_parses("dart", """
void main() {
  print('Hello, Dart!');
}
""")

def test_parse_dockerfile():
    assert_parses("dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
""")

def test_parse_doxygen():
    assert_parses("doxygen", """
/**
 * @brief A brief description of a function.
 *
 * This is a more detailed description of the function.
 * It can span multiple lines.
 *
 * @param name The name parameter
 * @return A greeting message
 */
""")

def test_parse_dtd():
    assert_parses("dtd", """
<!ELEMENT bookstore (book+)>
<!ELEMENT book (title, author, year, price)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT author (#PCDATA)>
<!ELEMENT year (#PCDATA)>
<!ELEMENT price (#PCDATA)>
<!ATTLIST book isbn CDATA #REQUIRED>
""")

def test_parse_elisp():
    assert_parses("elisp", """
(defun hello-world ()
  "Print a hello world message."
  (message "Hello, Emacs Lisp!"))

(hello-world)
""")

def test_parse_elixir():
    assert_parses("elixir", """
defmodule HelloWorld do
  def greet(name) do
    IO.puts("Hello, #{name}!")
  end
end

HelloWorld.greet("Elixir")
""")

def test_parse_elm():
    assert_parses("elm", """
module Main exposing (main)

import Html exposing (text)

main =
    text "Hello, Elm!"
""")

def test_parse_embeddedtemplate():
    assert_parses("embeddedtemplate", """
<h1>Welcome, <%= @user.name %></h1>
<% if @user.admin? %>
  <p>You have admin privileges.</p>
<% end %>
""")

def test_parse_erlang():
    assert_parses("erlang", """
-module(hello).
-export([hello_world/0]).

hello_world() ->
    io:format("Hello, World!~n").
""")

def test_parse_erlang_header():
    assert_parses("erlang", """
-ifndef(MYAPP_HEADER_H).
-define(MYAPP_HEADER_H, true).

-record(user, {id, name, email}).

-endif.
""")

def test_parse_fennel():
    assert_parses("fennel", """
(fn greet [name]
  (print (.. "Hello, " name "!")))

(greet "World")
""")

def test_parse_firrtl():
    assert_parses("firrtl", """
circuit MyModule :
  module MyModule :
    input clock : Clock
    input reset : UInt<1>
    output io : { flip in : UInt<8>, out : UInt<8> }

    io.out <= io.in
""")

def test_parse_fish():
    assert_parses("fish", """
function fish_greeting
    echo "Welcome to fish, the friendly interactive shell"
end

set -x PATH $HOME/bin $PATH
""")

def test_parse_fortran():
    assert_parses("fortran", """
program hello
    implicit none
    print *, "Hello, World!"
end program hello
""")

def test_parse_func():
    assert_parses("func", """
func main() {
    print("Hello, World!")
}
""")

def test_parse_gdscript():
    assert_parses("gdscript", """
extends Node

func _ready():
    print("Hello, Godot!")

func _process(delta):
    pass
""")

def test_parse_gitattributes():
    assert_parses("gitattributes", """
*.txt text
*.jpg binary
/src/main.cpp eol=lf
""")

def test_parse_gitcommit():
    assert_parses("gitcommit", """
Implement new feature X

- Added functionality Y
- Fixed bug Z

Closes #123
""")

def test_parse_gitignore():
    assert_parses("gitignore", """
# Ignore build output
/build/

# Ignore node modules
node_modules/

# Ignore log files
*.log
""")

def test_parse_gleam():
    assert_parses("gleam", """
pub fn main() {
    io.println("Hello from Gleam!")
}
""")

def test_parse_glsl():
    assert_parses("glsl", """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
""")

def test_parse_gn():
    assert_parses("gn", """
executable("hello_world") {
  sources = [ "hello_world.cc" ]
  deps = [ "//base" ]
}
""")

def test_parse_go():
    assert_parses("go", """
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
""")

def test_parse_gomod():
    assert_parses("gomod", """
module example.com/hello

go 1.16

require (
    github.com/gin-gonic/gin v1.7.4
    github.com/go-sql-driver/mysql v1.6.0
)
""")

def test_parse_gosum():
    assert_parses("gosum", """
github.com/gin-gonic/gin v1.7.4 h1:EmhMf+VfTeIuD1G/mDppLaLcbVqdHlvUFtqqhEfZ+Ik=
github.com/gin-gonic/gin v1.7.4/go.mod h1:jD2toBW3GZUr5UMcdrwQA10I7RuaFOl/SGeDjXkfUtY=
github.com/go-sql-driver/mysql v1.6.0 h1:BCTh4TKNUYmOmMUcQ3IipzF5prigylS7XXjEkfCHuOE=
github.com/go-sql-driver/mysql v1.6.0/go.mod h1:DCzpHaOWr8IXmIStZouvnhqoel9Qv2LBy8hT2VhHyBg=
""")

def test_parse_groovy():
    assert_parses("groovy", """
class Example {
    static void main(String[] args) {
        println 'Hello from Groovy!'
    }
}
""")

def test_parse_gstlaunch():
    assert_parses("gstlaunch", """
videotestsrc ! videoconvert ! autovideosink
""")

def test_parse_hack():
    assert_parses("hack", """
<<__EntryPoint>>
function main(): void {
  echo "Hello from Hack!\\n";
}
""")

def test_parse_hare():
    assert_parses("hare", """
use fmt;

export fn main() void = {
    fmt::println("Hello from Hare!");
};
""")

def test_parse_haskell():
    assert_parses("haskell", """
main :: IO ()
main = putStrLn "Hello from Haskell!"
""")

def test_parse_haxe():
    assert_parses("haxe", """
class Main {
    static function main() {
        trace("Hello from Haxe!");
    }
}
""")

def test_parse_hcl():
    assert_parses("hcl", """
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "HelloWorld"
  }
}
""")

def test_parse_heex():
    assert_parses("heex", """
<div>
  <h1>Hello from HEEX!</h1>
  <%= @message %>
</div>
""")

def test_parse_hlsl():
    assert_parses("hlsl", """
float4 PSMain(float4 position : SV_POSITION) : SV_TARGET
{
    return float4(1.0, 0.0, 0.0, 1.0); // Red color
}
""")

def test_parse_html():
    assert_parses("html", """
<!DOCTYPE html>
<html>
<head>
    <title>Hello, HTML!</title>
</head>
<body>
    <h1>Hello from HTML!</h1>
</body>
</html>
""")

def test_parse_hyprlang():
    assert_parses("hyprlang", """
general {
    border_size = 2
    gaps_in = 5
    gaps_out = 20
    col.active_border = rgba(33ccffee)
    col.inactive_border = rgba(595959aa)
}
""")

def test_parse_ispc():
    assert_parses("ispc", """
export void simple_add(uniform float vin[], uniform float vout[], uniform int count) {
    foreach (index = 0 ... count) {
        vout[index] = vin[index] + 1;
    }
}
""")

def test_parse_janet():
    assert_parses("janet", """
(defn fibonacci [n]
  (if (<= n 1)
    n
    (+ (fibonacci (- n 1))
       (fibonacci (- n 2)))))

(print (fibonacci 10))
""")

def test_parse_java():
    assert_parses("java", """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
""")

def test_parse_javascript():
    assert_parses("javascript", """
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("World"));
""")

def test_parse_javascript_module():
    assert_parses("javascript", """
export function greet(name) {
    return `Hello, ${name}!`;
}

import { greet } from './greet.mjs';
console.log(greet("World"));
""")

def test_parse_jsdoc():
    assert_parses("javascript", """
/**
 * Represents a book.
 * @constructor
 * @param {string} title - The title of the book.
 * @param {string} author - The author of the book.
 */
function Book(title, author) {
}

// Usage
let myBook = new Book("The Great Gatsby", "F. Scott Fitzgerald");
""")

def test_parse_json():
    assert_parses("json", """
{
  "name": "John Doe",
  "age": 30,
  "city": "New York"
}
""")

def test_parse_jsonnet():
    assert_parses("jsonnet", """
local person = {
  name: "Alice",
  welcome: "Hello " + self.name + "!",
};
{
  person: person,
  farewell: "Goodbye " + person.name + "!",
}
""")

def test_parse_julia():
    assert_parses("julia", """
function factorial(n::Integer)
    if n <= 1
        return 1
    else
        return n * factorial(n - 1)
    end
end

println(factorial(5))
""")

def test_parse_kconfig():
    assert_parses("kconfig", """
config EXAMPLE_FEATURE
    bool "Enable example feature"
    default y
    help
      This option enables the example feature.
      If unsure, say Y.
""")

def test_parse_kdl():
    assert_parses("kdl", """
person {
    name "John Doe"
    age 30
    address {
        street "123 Main St"
        city "Anytown"
    }
}
""")

def test_parse_kotlin():
    assert_parses("kotlin", """
fun main() {
    val name = "Kotlin"
    println("Hello, $name!")
}
""")

def test_parse_linkerscript():
    assert_parses("linkerscript", """
SECTIONS
{
  . = 0x10000;
  .text : { *(.text) }
  . = 0x8000000;
  .data : { *(.data) }
  .bss : { *(.bss) }
}
""")

def test_parse_llvm():
    assert_parses("llvm", """
define i32 @add(i32 %a, i32 %b) {
entry:
  %sum = add i32 %a, %b
  ret i32 %sum
}
""")

def test_parse_lua():
    assert_parses("lua", """
function factorial(n)
    if n == 0 then
        return 1
    else
        return n * factorial(n - 1)
    end
end

print(factorial(5))
""")

def test_parse_luadoc():
    assert_parses("lua", """
--- This is a simple function.
-- @param name string The name to greet.
-- @return string A greeting message.
function greet(name)
    return "Hello, " .. name .. "!"
end

-- Usage
print(greet("World"))
""")

def test_parse_luau():
    assert_parses("luau", """
local function tree_insert(tree, x)
    local lower, equal, greater = split(tree.root, x)
    if not equal then
        equal = {
            x = x,
            y = math.random(0, 2^31-1),
            left = nil,
            right = nil
        }
    end
    tree.root = merge3(lower, equal, greater)
end
""")

def test_parse_magik():
    assert_parses("magik", """
_package user
$

_method object.say_hello(name)
    _return write("Hello, ", name, "!")
_endmethod
$

_block
    object.say_hello("Magik")
_endblock
$
""")

def test_parse_make():
    assert_parses("make", """
CC = gcc
CFLAGS = -Wall -O2

all: hello

hello: hello.c
\t$(CC) $(CFLAGS) -o hello hello.c

clean:
\trm -f hello
""")

def test_parse_markdown():
    assert_parses("markdown", """
# Hello, Markdown!

This is a simple Markdown document.

- Item 1
- Item 2

**Bold text** and *italic text*.

[A link](https://example.com)
""")

def test_parse_mermaid():
    assert_parses("mermaid", """
stateDiagram
    direction LR
    [*] --> A
    A --> B
    B --> C
    state B {
        direction LR
        a --> b
    }
    B --> D
""")

def test_parse_meson():
    assert_parses("meson", """
project('hello', 'c')

executable('hello',
           sources : ['hello.c'],
           install : true)
""")

def test_parse_ninja():
    assert_parses("ninja", """
cflags = -Wall

rule cc
  command = gcc $cflags -c $in -o $out

build foo.o: cc foo.c
""")

def test_parse_nix():
    assert_parses("nix", """
{ stdenv, fetchurl }:

stdenv.mkDerivation rec {
  pname = "hello";
  version = "2.10";

  src = fetchurl {
    url = "mirror://gnu/hello/${pname}-${version}.tar.gz";
    sha256 = "0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i";
  };

  doCheck = true;

  meta = with stdenv.lib; {
    description = "A program that produces a familiar, friendly greeting";
    homepage = "https://www.gnu.org/software/hello/";
    license = licenses.gpl3Plus;
    platforms = platforms.all;
  };
}
""")

def test_parse_nqc():
    assert_parses("nqc", """
task main()
{
    OnFwd(OUT_A);
    Wait(100);
    Off(OUT_A);
}
""")

def test_parse_objc():
    assert_parses("objc", """
#import <Foundation/Foundation.h>

@interface Greeter : NSObject
- (void)sayHello:(NSString *)name;
@end

@implementation Greeter
- (void)sayHello:(NSString *)name {
    NSLog(@"Hello, %@!", name);
}
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Greeter *greeter = [[Greeter alloc] init];
        [greeter sayHello:@"Objective-C"];
    }
    return 0;
}
""")

def test_parse_odin():
    assert_parses("odin", """
package main

import "core:fmt"

main :: proc() {
    fmt.println("Hello, Odin!")
}
""")

def test_parse_org():
    assert_parses("org", """
#+TITLE: Hello, Org Mode!

* First Heading
** Subheading
   Some text here.

* TODO Learn more about Org Mode
  DEADLINE: <2023-12-31 Sun>

* Code Block
  #+BEGIN_SRC python
  def hello(name):
      print(f"Hello, {name}!")

  hello("Org Mode")
  #+END_SRC
""")

def test_parse_pascal():
    assert_parses("pascal", """
program Hello;
begin
  writeln ('Hello, World!');
end.
""")

# The following is a self-signed certificate, generated with the following command:
# openssl req -x509 -newkey ec:<(openssl ecparam -name prime256v1) -nodes -days 365 -subj "/C=US/ST=State/L=City/O=Organization/CN=example.com" -keyout /dev/null 2>/dev/null
def test_parse_pem():
    assert_parses("pem", """
-----BEGIN CERTIFICATE-----
MIICBzCCAa2gAwIBAgIUHnsM82Dk9y+hFxaQ1cEDBW2YWgkwCgYIKoZIzj0EAwIw
WTELMAkGA1UEBhMCVVMxDjAMBgNVBAgMBVN0YXRlMQ0wCwYDVQQHDARDaXR5MRUw
EwYDVQQKDAxPcmdhbml6YXRpb24xFDASBgNVBAMMC2V4YW1wbGUuY29tMB4XDTI0
MDgyMjIzNTEzNVoXDTI1MDgyMjIzNTEzNVowWTELMAkGA1UEBhMCVVMxDjAMBgNV
BAgMBVN0YXRlMQ0wCwYDVQQHDARDaXR5MRUwEwYDVQQKDAxPcmdhbml6YXRpb24x
FDASBgNVBAMMC2V4YW1wbGUuY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE
wI+acYHilbDhamCyICG6iksKykR4C2t1z+AYzNnij2RkF5nnjhAzNwncBtsX8TDV
RWPRE+/e5tb2hn2M1ALYw6NTMFEwHQYDVR0OBBYEFD/wtrQGnnLep6/HV96HfXI5
ugjiMB8GA1UdIwQYMBaAFD/wtrQGnnLep6/HV96HfXI5ugjiMA8GA1UdEwEB/wQF
MAMBAf8wCgYIKoZIzj0EAwIDSAAwRQIgEtptEtlFf356WbrUAN2Uu4CDpNuYIHMe
G/y2eHrHV9cCIQCjjI6awvvdDB6RVClVFBsBK//sY95JWMdk+Dt2CfldDQ==
-----END CERTIFICATE-----
""")

def test_parse_perl():
    assert_parses("perl", """
#!/usr/bin/perl
use strict;
use warnings;

print "Hello, World!\n";
""")

def test_parse_perl_module():
    assert_parses("perl", """
package MyModule;

use strict;
use warnings;

sub new {
    my $class = shift;
    my $self = {};
    bless $self, $class;
    return $self;
}

1;
""")

def test_parse_pgn():
    assert_parses("pgn", """
[Event "F/S Return Match"]
[Site "Belgrade, Serbia JUG"]
[Date "1992.11.04"]
[Round "29"]
[White "Fischer, Robert J."]
[Black "Spassky, Boris V."]
[Result "1/2-1/2"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 {This opening is called the Ruy Lopez.}
4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7
11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5
Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6
23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5
hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5
35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6
Nf2 42. g4 Bd3 43. Re6 1/2-1/2
""")

def test_parse_php():
    assert_parses("php", """
<?php
function greeting($name) {
    return "Hello, " . $name . "!";
}

echo greeting("World");
?>
""")

def test_parse_po():
    assert_parses("po", """
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2023-06-14 10:30+0200\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Hello, World!"
msgstr "Bonjour, le monde!"
""")

def test_parse_pony():
    assert_parses("pony", """
actor Main
  new create(env: Env) =>
    env.out.print("Hello, World!")
""")

def test_parse_powershell():
    assert_parses("powershell", """
function Get-Greeting {
    param (
        [string]$Name = "World"
    )
    "Hello, $Name!"
}

Get-Greeting
""")

def test_parse_powershell_module():
    assert_parses("powershell", """
function Get-Greeting {
    param (
        [string]$Name = "World"
    )
    "Hello, $Name!"
}

Export-ModuleMember -Function Get-Greeting
""")

def test_parse_printf():
    assert_parses("printf", """
Hello, %s!
""")

def test_parse_prisma():
    assert_parses("prisma", """
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  content   String?
  published Boolean @default(false)
  author    User    @relation(fields: [authorId], references: [id])
  authorId  Int
}
""")

def test_parse_properties():
    assert_parses("properties", """
# This is a comment
key1=value1
key2 = value2
key.3: value3
""")

def test_parse_psv():
    assert_parses("psv", """
Name|Age|City
John|30|New York
Alice|25|London
Bob|35|Paris
""")

def test_parse_puppet():
    assert_parses("puppet", """
class greeting {
  $recipient = 'World'

  file { '/tmp/hello':
    ensure  => present,
    content => "Hello, ${recipient}!",
  }
}

include greeting
""")

def test_parse_purescript():
    assert_parses("purescript", """
module Main where

import Effect.Console (log)

main = log "Hello, World!"
""")

def test_parse_pymanifest():
    assert_parses("pymanifest", """
# This is a sample MANIFEST.in file
include README.md
include LICENSE
recursive-include examples *.txt *.py
recursive-include src *.py
recursive-include tests *.py
global-exclude *.pyc
global-exclude __pycache__
prune build
prune dist
""")

def test_parse_python():
    assert_parses("python", """
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("World"))
""")

def test_parse_qmldir():
    assert_parses("qmldir", """
Module MyModule
MyType 1.0 MyType.qml
singleton MySingleton 1.0 MySingleton.qml
classname MyPlugin
depends QtQuick 2.0
""")

def test_parse_qmljs():
    assert_parses("qmljs", """
import QtQuick 2.0

Rectangle {
    width: 200
    height: 100
    color: "red"

    Text {
        anchors.centerIn: parent
        text: "Hello, QML!"
    }
}
""")

def test_parse_r():
    assert_parses("r", """
# Function to calculate the mean of a vector
calculate_mean <- function(x) {
  if (length(x) == 0) {
    return(NA)
  }
  return(sum(x) / length(x))
}

# Example usage
numbers <- c(1, 2, 3, 4, 5)
result <- calculate_mean(numbers)
print(paste("The mean is:", result))
""")

def test_parse_racket():
    assert_parses("racket", """
#lang racket

(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(display (factorial 5))
(newline)
""")

# def test_parse_re2c():
#     assert_parses("re2c", """
# #include <stdio.h>
# #include <stdlib.h>

# /*!re2c
#     [0-9]+ { return 10; }
#     [a-z]+ { return 20; }
#     [ \t]  { return 0; }
#     *      { return -1; }
# */

# int main() {
#     return 0;
# }
# """)

def test_parse_readline():
    assert_parses("readline", """
# Turn on VI editing mode
set editing-mode vi

# Show all completions as soon as I press tab, even if there's more than one
set show-all-if-ambiguous on

# Ignore case
set completion-ignore-case on

# on menu-complete, first display the common prefix, then cycle through the options when hitting TAB
set menu-complete-display-prefix on
""")

def test_parse_requirements():
    assert_parses("requirements", """
# This is an example requirements file
Django==3.2.4
requests>=2.25.1,<3.0.0
numpy~=1.20.0
pandas
matplotlib>=3.4.0
""")

def test_parse_ron():
    assert_parses("ron", """
GameConfig(
    window_size: (800, 600),
    window_title: "My Awesome Game",
    fullscreen: false,
    vsync: true,
    max_fps: 60,
    player: Player(
        name: "Hero",
        max_health: 100,
        attack_power: 10,
    ),
    enemies: [
        Enemy(type: "Goblin", health: 30, damage: 5),
        Enemy(type: "Orc", health: 50, damage: 8),
    ],
)
""")

def test_parse_rst():
    assert_parses("rst", """
=======================
My Document Title
=======================

Section 1
=========

This is a paragraph in section 1.

- Bullet point 1
- Bullet point 2

Section 2
=========

This is a paragraph in section 2.

.. code-block:: python

   def hello_world():
       print("Hello, World!")

""")

def test_parse_ruby():
    assert_parses("ruby", """
class Greeter
  def initialize(name)
    @name = name
  end

  def greet
    puts "Hello, #{@name}!"
  end
end

greeter = Greeter.new("World")
greeter.greet
""")

def test_parse_rust():
    assert_parses("rust", """
fn main() {
    let greeting = "Hello, Rust!";
    println!("{}", greeting);

    let numbers = vec![1, 2, 3, 4, 5];
    let sum: i32 = numbers.iter().sum();
    println!("Sum of numbers: {}", sum);
}
""")

def test_parse_scala():
    assert_parses("scala", """
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, Scala!")

    val numbers = List(1, 2, 3, 4, 5)
    val doubled = numbers.map(_ * 2)
    println(s"Doubled numbers: $doubled")
  }
}
""")

def test_parse_scheme():
    assert_parses("scheme", """
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(display (factorial 5))
(newline)

(define (fibonacci n)
  (if (< n 2)
      n
      (+ (fibonacci (- n 1)) (fibonacci (- n 2)))))

(display (map fibonacci '(0 1 2 3 4 5 6 7 8 9)))
(newline)
""")

def test_parse_scss():
    assert_parses("scss", """
$primary-color: #3498db;

.button {
  background-color: $primary-color;
  color: white;
  padding: 10px 15px;
  &:hover {
    background-color: darken($primary-color, 10%);
  }
}
""")

def test_parse_smali():
    assert_parses("smali", """
.class public Lcom/example/HelloWorld;
.super Ljava/lang/Object;

.method public static main([Ljava/lang/String;)V
    .registers 2
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;
    const-string v1, "Hello, World!"
    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V
    return-void
.end method
""")

def test_parse_smithy():
    assert_parses("smithy", """
namespace example.weather

use aws.protocols#restJson1

@restJson1
service Weather {
    version: "2006-03-01"
    operations: [GetCurrentTime]
}

operation GetCurrentTime {
    output: GetCurrentTimeOutput
}

structure GetCurrentTimeOutput {
    @required
    time: Timestamp
}
""")

def test_parse_solidity():
    assert_parses("solidity", """
pragma solidity ^0.8.0;

contract HelloWorld {
    string public message;

    constructor() {
        message = "Hello, World!";
    }

    function setMessage(string memory newMessage) public {
        message = newMessage;
    }
}
""")

def test_parse_sql():
    assert_parses("sql", """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO users (username, email) VALUES ('john_doe', 'john@example.com');

SELECT * FROM users WHERE username = 'john_doe';
""")

def test_parse_squirrel():
    assert_parses("squirrel", """
function greet(name) {
    print("Hello, " + name + "!");
}

local world = "World";
greet(world);
""")

def test_parse_starlark():
    assert_parses("starlark", """
def greet(name):
    return "Hello, " + name + "!"

def main():
    print(greet("World"))

if __name__ == "__main__":
    main()
""")

def test_parse_svelte():
    assert_parses("svelte", """
<script>
  let name = 'world';
</script>

<h1>Hello {name}!</h1>

<style>
  h1 {
    color: blue;
  }
</style>
""")

def test_parse_swift():
    assert_parses("swift", """
import Foundation

func greet(name: String) -> String {
    return "Hello, \\(name)!"
}

print(greet(name: "World"))
""")

def test_parse_tablegen():
    assert_parses("tablegen", """
class Instruction<bits<32> op, string asmstr> {
  bits<32> Opcode = op;
  string AsmString = asmstr;
}

def ADD : Instruction<0b00000000000000000000000000100000, "add $rd, $rs, $rt">;
""")

def test_parse_tcl():
    assert_parses("tcl", """
proc greet {name} {
    return "Hello, $name!"
}

puts [greet "World"]
""")

def test_parse_thrift():
    assert_parses("thrift", """
namespace cpp example
namespace py example

struct Person {
  1: string name,
  2: i32 age,
  3: bool active
}

service PersonService {
  Person getPerson(1: string name)
}
""")

def test_parse_toml():
    assert_parses("toml", """
[package]
name = "my_package"
version = "0.1.0"
authors = ["Jane Doe <jane@example.com>"]

[dependencies]
serde = "1.0"
tokio = { version = "1.0", features = ["full"] }
""")

def test_parse_tsv():
    assert_parses("tsv", """
Name\tAge\tCity
John Doe\t30\tNew York
Jane Smith\t25\tLos Angeles
Bob Johnson\t45\tChicago
""")

def test_parse_tsx():
    assert_parses("tsx", """
import React from 'react';

interface GreetingProps {
  name: string;
}

const Greeting: React.FC<GreetingProps> = ({ name }) => {
  return <h1>Hello, {name}!</h1>;
};

export default Greeting;
""")

def test_parse_twig():
    assert_parses("twig", """
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    {% for item in items %}
        <p>{{ item }}</p>
    {% endfor %}
</body>
</html>
""")

def test_parse_typescript():
    assert_parses("typescript", """
function greet(name: string): string {
    return `Hello, ${name}!`;
}

const world: string = "World";
console.log(greet(world));
""")

def test_parse_typst():
    assert_parses("typst", """
#let project(title, authors, body) = {
  set document(author: authors, title: title)
  set page(numbering: "1", number-align: center)

  align(center)[
    #block(text(weight: 700, 1.75em, title))
    #block(text(1.25em, authors))
  ]

  body
}

#show: project.with(
  title: "My Document",
  authors: (
    "Jane Doe",
  ),
)

= Introduction
This is a sample Typst document.
""")

def test_parse_udev():
    assert_parses("udev", """
# This is a sample udev rule
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d6b", ATTRS{idProduct}=="0001", MODE="0666"
""")

def test_parse_ungrammar():
    assert_parses("ungrammar", """
Grammar =
  Node*

Node =
  name:'ident' '=' Rule

Rule =
  'ident'
| 'token_ident'
| Rule*
| Rule ('|' Rule)*
| Rule '?'
| Rule '*'
| '(' Rule ')'
| label:'ident' ':' Rule

Expr =
  literal
| lhs:Expr op:('+' | '-' | '*' | '/') rhs:Expr
""")

def test_parse_uxntal():
    assert_parses("uxntal", """
|00 @System ( vector 0100 )
|10 @Console ( vector 0110 )

|0100 ( -> )
    ;on-reset JMP2

|0110 ( -> )
    LIT "H" #18 DEO
    LIT "i" #18 DEO
    BRK

|0200
@on-reset ( -> )
    ;Console .vector DEO2
    BRK
""")

def test_parse_verilog():
    assert_parses("verilog", """
module counter(
    input clk,
    input reset,
    output reg [3:0] count
);
    always @(posedge clk or posedge reset) begin
        if (reset)
            count <= 4'd0;
        else
            count <= count + 1;
    end
endmodule
""")

def test_parse_vhdl():
    assert_parses("vhdl", """
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity counter is
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           count : out STD_LOGIC_VECTOR (3 downto 0));
end counter;

architecture Behavioral of counter is
    signal count_int : unsigned(3 downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            count_int <= (others => '0');
        elsif rising_edge(clk) then
            count_int <= count_int + 1;
        end if;
    end process;

    count <= std_logic_vector(count_int);
end Behavioral;
""")

def test_parse_vim():
    assert_parses("vim", """
function! Greet(name)
    echo "Hello, " . a:name . "!"
endfunction

command! -nargs=1 Greet call Greet(<q-args>)

nnoremap <leader>g :Greet World<CR>
""")

def test_parse_vue():
    assert_parses("vue", """
<template>
  <div>
    <h1>{{ greeting }}</h1>
    <button @click="changeGreeting">Change Greeting</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      greeting: 'Hello, Vue!'
    }
  },
  methods: {
    changeGreeting() {
      this.greeting = 'Hello, World!'
    }
  }
}
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
""")

def test_parse_wgsl():
    assert_parses("wgsl", """
struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
};

@vertex
fn vs_main(@location(0) position: vec3<f32>) -> VertexOutput {
    var out: VertexOutput;
    out.position = vec4<f32>(position, 1.0);
    out.color = vec4<f32>(1.0, 0.0, 0.0, 1.0);
    return out;
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    return in.color;
}
""")

def test_parse_xcompose():
    assert_parses("xcompose", """
include "%L"

<Multi_key> <colon> <parenright> : "☺"   U263A           # WHITE SMILING FACE
<Multi_key> <colon> <parenleft>  : "☹"   U2639           # WHITE FROWNING FACE
<Multi_key> <less> <3>           : "♥"   U2665           # BLACK HEART SUIT
""")

def test_parse_xml():
    assert_parses("xml", """
<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
  <book category="cooking">
    <title lang="en">Everyday Italian</title>
    <author>Giada De Laurentiis</author>
    <year>2005</year>
    <price>30.00</price>
  </book>
  <book category="children">
    <title lang="en">Harry Potter</title>
    <author>J K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
</bookstore>
""")

def test_parse_yaml():
    assert_parses("yaml", """
---
# An employee record
name: John Doe
age: 30
position: Developer
skills:
  - Python
  - JavaScript
  - Docker
address:
  street: 123 Main St
  city: Anytown
  country: USA
""")

def test_parse_yuck():
    assert_parses("yuck", """
(defwindow example
  :monitor 0
  :geometry (geometry :x "0%"
                      :y "0%"
                      :width "90%"
                      :height "30px"
                      :anchor "top center")
  :stacking "fg"
  :reserve (struts :distance "40px" :side "top")
  :windowtype "dock"
  :wm-ignore false
  (box :class "example-box"
       :orientation "h"
       (button :onclick "xdg-open https://github.com/elkowar/eww"
               "Open eww repository")))
""")

def test_parse_zig():
    assert_parses("zig", """
const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s}!\n", .{"Zig"});
}
""")

#!/usr/bin/env bats

@test "Check Home page" {
  curl -sfq localhost:8000/ | grep -F Hello
}

@test "Check version URL" {
  curl -sfq localhost:8000/version
}

@test "Check version URL Content" {
  curl -sfq localhost:8000/version | grep -F "$GITHUB_SHA"
}

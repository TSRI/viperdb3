#!/bin/bash

if [[ $(ruby -e 'print RUBY_VERSION') != '1.9.3' ]]; then
  \curl -L https://get.rvm.io | bash -s stable --ruby=1.9.3
  source ~/.rvm/scripts/rvm
  rvm install 1.9.3
  rvm install 1.9.3 --default
fi

if [[ $(gem -v) != '1.8.11' ]]; then
  rvm rubygems current
  sudo update-alternatives --set gem /usr/bin/gem1.9.1
fi
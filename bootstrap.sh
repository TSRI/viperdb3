#!/bin/bash

if [[ $(ruby -e 'print RUBY_VERSION') != '1.9.3' ]]; then
  \curl -L https://get.rvm.io | bash -s stable --ruby=1.9.3
  source ~/.rvm/scripts/rvm
  rvm install 1.9.3
  rvm install 1.9.3 --default
fi

if [[ $(gem -v) != '1.8.25' ]]; then
  rvm rubygems current
  sudo update-alternatives --set gem /usr/bin/gem1.9.1
  gem install bundler
  bundle install
fi

if [[ $(which berks) ]]; then
  berks install -p /usr/local/lib/viperdb3/cookbooks/
fi

if which chef-solo >/dev/null; then
  sudo /usr/local/bin/chef-solo -c solo.rb -j node.json
else
  sudo true && curl -L https://www.opscode.com/chef/install.sh | sudo bash
fi


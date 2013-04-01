#!/usr/bin/env ruby
require 'rubygems'
require 'json'
require 'time'
require 'pcap'
require 'http'
require 'nokogiri'
include Pcap

$pcapname = "../victim_no22full.pcap"
$jsonname = "/data/netflow/jsons/uj/2012.json"

$http = Net::HTTP.new('www.ictf2013.net', 80)
$path = '/submit_netflow'
$url = URI.parse("http://www.ictf2013.net/submit_netflow")
$cookie = 'session=****&csrf=*****&user_id=*******";'

def send_pkg netflow_id

  req = Net::HTTP::Get.new($url.path, {
    "Cookie" => $cookie
  })
  csrf_token = Nokogiri::HTML(Net::HTTP.start($url.host, $url.port){ |http| 
    http.request(req)
  }.body).css('input').inject(''){ |token,element| element.attr('type') == 'hidden' ? element.attr('value') : token }
  data = "netflow_id=#{netflow_id}&csrf_token=#{csrf_token}"
  headers = {
    'Cookie' => $cookie,
  }
  $http.post($path, data, headers)
end

$json = JSON.parse(File.read($jsonname))
def get_netflow_id sport, time
  filtered = $json["netflows"].select { |x| 
    x["source_port"] == sport.to_s && (Time.parse(x["created_timestamp"]).to_i-time+28800).abs < 20
  }
  if filtered.length == 1
    return filtered[0]['id']
  else
    return nil
  end
end


def get_tcp_flow(seq)
  pkgs = []
  Pcap::Capture.open_offline($pcapname).each{ |pkg| 
    pkgs << pkg if pkg.tcp? && pkg.tcp_seq == seq
  }
  pkgs
end

def detect6699(pkg_first)
  data = pkg_first.tcp_data.to_s[0..39]
  Pcap::Capture.open_offline($pcapname).each{ |pkg| 
    return true if pkg.tcp? && pkg.time_i >= pkg_first.time_i && (pkg.time_i-pkg_first.time_i).abs<2 && pkg.dport==pkg_first.dport && pkg.ip_id != pkg_first.ip_id && pkg.tcp_data.to_s[0..39]==data
  }
  false
end

$f=0
Pcap::Capture.open_offline($pcapname).each{ |pkg| 
  #sport, dport, tcp?, tcp_data
  if pkg.tcp? && pkg.tcp_data
	found = false
    data = pkg.tcp_data
	port = pkg.sport
    if pkg.sport == 4444 && data =~ /ARE YOU CRAZY/
	  found = true
	  port = pkg.dport
    end
	if pkg.dport == 8089 && data =~ /metadata/ && data =~ /fileRead/
		found = true
	end
	if pkg.sport == 2583 && data =~ /GOVERNMENT/
		found = true
        port = pkg.dport
	end
    if pkg.dport == 6699
      found = false#detect6699(pkg)	  
    end
    if pkg.dport == 8888 && data =~ /username=%27/
	  found = true
    end
	
	if found && get_netflow_id(port, pkg.time_i)
	  nid = get_netflow_id(port, pkg.time_i)
      puts "#{pkg.time_i}: #{pkg.sport} -> #{pkg.dport}: #{data[0..10]}    ||| id(#{port}, #{pkg.time_i}"
	  puts "NETFLOW ID: " + nid.to_s
	 # get_tcp_flow(pkg.tcp_seq).each{ |asd|
	 #   puts "#{asd.time_i}: #{asd.sport} -> #{asd.dport}: #{data[0..10]}"
	 # }
      #puts (send_pkg(nid)).body
	end
  end
}

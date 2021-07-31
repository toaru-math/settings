会社でUbuntuを使うときに必要なプロキシの設定をまとめました。   

本記事でのプロキシサーバ（FQDN+ポート番号）は`proxy-server:port`で表記します。  
ご使用のプロキシ環境に合わせて読み替えて設定ください。


<b>目次</b>  
[:contents]


# 全般
環境変数を設定することで概ね解決します。  
`~/.bashrc`などに書いておくとよいです。編集後は`source ~/.bashrc`をお忘れなく。
```
export http_proxy="http://proxy-server:port/"
export https_proxy="http://proxy-server:port/"
export HTTP_PROXY=${http_proxy}
export HTTPS_PROXY=${https_proxy}
```

`sudo`コマンドを使うときは`-E`オプションを付加することで、実行ユーザの環境変数を引き継ぐことができます。
```
$ sudo apt-get update       #環境変数が引き継がれないのでプロキシ未指定の状態
$ sudo -E apt-get update    #実行ユーザの環境変数を引き継ぐのでプロキシが通る
```


プロキシの例外は以下のように設定します。
```
export no_porxy="localhost,192.168.0.1,.localserver.com"
export NO_PROXY=${no_proxy}
```
残念なことに、ワイルドカードやCIDR記法による設定ができないようです。  
個別のIPアドレスかドメイン名をカンマ区切りで入力する必要があります。  
以下のようにして展開することができますが、入力数が多いと正しく動作しない場合があるそうなので、必要最小限で設定するのが安全です。
```
printf -v ip_addrs '%s,' 192.168.{0..255}.{0..255}
export no_proxy="${ip_addrs%,}"
```


# apt-get / apt
2通りの方法があります。

- 環境変数の設定
- apt.confの設定

`/etc/apt/apt.conf` に以下のように追記してプロキシサーバを指定します。  

```
Acquire::ftp::proxy "ftp://proxy-server:port/";
Acquire::http::proxy "http://proxy-server:port/";
Acquire::https::proxy "http://proxy-server:port/";
```
編集後は即座に設定が反映されます。  
※ `apt.conf`がある場合は環境変数よりも優先されます。

尚、他のapt系のコマンドには反映されないようなので、個別に設定するかコマンドのオプションでプロキシサーバを指定する必要があります。


# wget
2通りの方法があります。

- 環境変数の設定
- .wgetrcの設定

`~/.wgetrc` に以下のように追記してプロキシサーバを指定します。 

```
http_proxy  = http://proxy-server:port/
https_proxy = http://proxy-server:port/
```
編集後は即座に設定が反映されます。  
※ `.wgetrc`がある場合は環境変数よりも優先されます。  
ユーザ全体に対して設定する場合は`/etc/wgetrc`に対して設定します。  

証明書チェックでコケる場合は`--no-check-certificate`オプションで証明書のチェックをスキップできます。（スキップは自己責任で）

```
$ wget --no-check-certificate https://url
```


# curl
2通りの方法があります。

- 環境変数の設定
- .curlrcの設定

`~/.curlrc` に以下のように追記してプロキシサーバを指定します。 
```
http_proxy = "http://proxy-server:port/"
```
編集後は即座に設定が反映されます。  
※ `.curlrc`がある場合は環境変数よりも優先されます。  

証明書チェックでコケる場合は`~/.curlrc`に以下を追記することで証明書のチェックをスキップできます。（スキップは自己責任で）
```
insecure
```


# git
3通りの方法があります。

- 環境変数の設定
- .gitconfigの設定
- リポジトリ内の.git/configの設定  


`~/.gitconfig` に以下のように追記してプロキシサーバを指定します。 
```
[http]
        proxy = http://proxy-server:port/
[https]
        proxy = http://proxy-server:port/
```

編集後は即座に設定が反映されます。  
※ `.gitconfig`がある場合は環境変数よりも優先されます。    

この設定はコマンドラインから行うこともできます。
```
$ git config --global http.proxy http://proxy.server:port/
$ git config --global https.proxy http://proxy.server:port/
```

リポジトリ内の`.git/config` に以下のように追記してプロキシサーバを指定することもできます。
```
$ git config --local http.proxy http://proxy.server:port/
$ git config --local https.proxy http://proxy.server:port/
```

設定の優先順位は以下の通りです。  
`.git/config` > `~/.gitconfig` > 環境変数


# pip
2通りの方法があります。

- 環境変数の設定
- pip.confの設定

`~/.config/pip/pip.conf` に以下のように追記してプロキシサーバを指定します。   
バージョンによっては`~/.pip/pip.conf`に追記するかもしれません。
```
[global]
proxy = http://proxy-server:port/
```
編集後は即座に設定が反映されます。  
※ `pip.conf`がある場合は環境変数よりも優先されます。    

証明書チェックでコケる場合は、信頼するサイトを`pip.conf`に登録します。
```
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org

```



# docker
pull/buildに対する設定です。 各コンテナへの設定は上記と同様に行えばOKです。 
daemonであるdockerdプロセスに対してプロキシサーバを指定します。  
`/etc/systemd/system/docker.service.d/http-proxy.conf`に以下を追記します。   
（ファイル／ディレクトリがなければ作成します。）
```
[Service]
Environment="HTTP_PROXY=http://proxy-server:port/"
```


設定を有効にするために以下のコマンドを実行します。
```
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```


# Tips
## https_proxy の設定は http or https ？
設定による違いはプロキシサーバとの秘匿通信を行うか否か。    

プロキシサーバと秘匿通信を行わない場合は以下のように設定する。  
（環境変数による設定に限りません。）
```
export http_proxy="http://proxy-server:port/"
export https_proxy="http://proxy-server:port/"
```

プロキシサーバと秘匿通信を行う場合は以下のように設定する。  
```
export http_proxy="https://proxy-server:port/"
export https_proxy="https://proxy-server:port/"
```

会社のプロキシサーバは通信の検閲を行う目的もあることが多く、秘匿通信の場合はコネクションを切られてプロキシの外に出れないことがあります。

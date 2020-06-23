# -*- coding: utf-8 -*-
import subprocess, os, time
import setting
from multiprocessing.dummy import Pool as ThreadPool
from utils.other.get_initobj import initobj

# 多线程处理数据
bashpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class CollectionThread(object):
    def __init__(self, data, oid_name):
        """
        :param data: 单个实例ip 团体字信息
        :param oid_name: 配置文件中的oid—name
        """

        self.oid_name = oid_name
        self.data = data
        self.ip = self.data[setting.ip]  # ip
        self.community = self.data[setting.community]  # 团体字
        self.instanceId = data['instanceId']  # 实例中实例ID
        self.name = data['name']  # 实例中的名字 TODO 可能这里有人不叫name
        if setting.switc in ('on', 'deal', 'insert'):  # 配置文件中，按照策略执行命令
            self._mkdir()  # 初始化目录文件
            # 数据解析配置类
            if oid_name == setting.plugins_oid.keys()[0]:
                self.analysisobj = initobj(path='plugins.DealDataPlugins', class_name=self.oid_name)  # 动态加载公共处理脚本类

            elif oid_name == setting.plugins_oid.keys()[1]:
                self.analysisobj = initobj(path='plugins.DealDataPlugins', class_name=self.oid_name)  # 动态加载公共处理脚本类

        self.dealdatas = {}  # 解析完后的数据（未合并状态）
        self.timeout_ip = []  # 执行shell命令超时的IP

    # 入口
    def run(self):
        self.snmp_run()
        # 关闭线程,
        self.async_pool.close()

        # 把超时的ip加入到self.dealdatas里面, 去重
        self.dealdatas.update({"timeout_ip": list(set(self.timeout_ip))})
        # 把实例对象ID加入数据中
        self.dealdatas.update({"instanceId": self.instanceId})
        # 把ip信息加入总数据里面
        self.dealdatas.update({"ip_info": self.data})

        return self.dealdatas

    # 拼接执行命令
    def snmp_run(self):
        cmds = []
        oid_name_list = []
        # 配置文件中的oid
        alloidname = setting.plugins_oid[self.oid_name]
        for k, v in alloidname.items():
            # 保存命令
            cmds.append("snmpwalk -v 2c -c {0} {1} {2}".format(self.community, self.ip, v))
            oid_name_list.append(k)

        self.async_pool = ThreadPool(setting.pool_nums if len(cmds) > setting.pool_nums else len(cmds))  # 线程池
        # 执行线程
        results = []
        for index, cmd in enumerate(cmds):
            result = self.async_pool.apply_async(self.deal_snmp, args=(cmd, oid_name_list[index]))
            results.append(result)

        # 执行线程
        for i in results:
            i.wait()  # 等待线程函数执行完毕

    # 执行命令
    def deal_snmp(self, cmd, name):
        """
        :param cmd: 单条命令
        :param name: oid名字
        :return:
        """
        # 取现网数据
        if setting.switc in ('on', 'deal', 'insert'):
            # 执行命令
            try:
                # data = subprocess.check_output(cmd, shell=True).decode()
                data = self._run_command(cmd, timeout=setting.timeout)
            except subprocess.CalledProcessError as e:
                data = ''
            except Exception as e:
                data = ''

        # 读取本地数据
        else:
            try:
                path = bashpath + '/data/' + self.ip + '/' + name
                with open(path, 'r') as f:
                    data = f.read()
            except Exception as e:
                data = ''

        # t = threading.currentThread()
        # print "进程ID：%s, 线程ID %s" % (os.getpid(), t.ident), 'Thread name : %s' % t.getName()

        self._dealalldata(name, data)

    # 根据策略处理数据
    def _dealalldata(self, name, data):
        if setting.switc == 'on':
            # 1.现网保存数据到data目录下
            self._createdata(name, data)

        elif setting.switc == 'deal':
            # 保存数据到data，并上次数据到cmdb中，要写到setting里面配置
            self._createdata(name, data)
            deal_data = getattr(self.analysisobj, name)(data)
            self.dealdatas.update(deal_data)

        # elif setting.switc == 'insert':
        #     # 获取现网数据，解析格式后汇报到cmdb
        #     getattr(self.analysisobj, name)(data)

        else:
            # 打印本地data数据
            print (self.ip, name, data)

    # 采集的数据放入data
    def _createdata(self, name, data):
        """
        保存采集的数据到data目录下
        :param args: (data, oidname)
        :return:
        """

        datapath = self.ippath + '/' + name
        with open(datapath, 'w') as f:
            f.write(data)

    # 创建目录
    def _mkdir(self):
        """
        创建目录
        :return:
        """
        self.ippath = bashpath + '/data/' + self.ip
        if not os.path.exists(self.ippath):
            os.mkdir(self.ippath)

    def _run_command(self, cmd, timeout=60):
        """执行命令cmd，返回命令输出的内容。
        如果超时将会抛出TimeoutError异常。
        cmd - 要执行的命令
        timeout - 最长等待时间，单位：秒
        """
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        t_beginning = time.time()
        while True:
            if p.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                # 记录超时的机器ip
                self.timeout_ip.append(cmd.split(' ')[-2])
                return ''
            time.sleep(0.1)
        return p.stdout.read()



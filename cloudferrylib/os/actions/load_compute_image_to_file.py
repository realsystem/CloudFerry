import os
from fabric.api import run, settings, env
from cloudferrylib.base.action import action
from cloudferrylib.utils import cmd_cfg
from cloudferrylib.utils import forward_agent
from cloudferrylib.utils import utils as utl

INSTANCES = 'instances'
DIFF = 'diff'
EPHEMERAL = 'ephemeral'
DIFF_OLD = 'diff_old'
EPHEMERAL_OLD = 'ephemeral_old'
PATH_DST = 'path_dst'
HOST_DST = 'host_dst'
PATH_SRC = 'path_src'
HOST_SRC = 'host_src'


class LoadComputeImageToFile(action.Action):
    def run(self, info=None, **kwargs):
        cfg = self.cloud.cloud_config.cloud
        temp_dir_name = os.popen('mktemp -udt image_dir_XXXX').read().rstrip()
        cfg.image_temp = temp_dir_name
        image_dir_cmd = cmd_cfg.mkdir_cmd(temp_dir_name)
        self.cloud.ssh_util.execute(image_dir_cmd)
        for instance_id, instance in info[utl.INSTANCES_TYPE].iteritems():
            image_id = info[INSTANCES][instance_id][utl.INSTANCE_BODY]['image_id']
            base_file = "%s/%s" % (temp_dir_name, "temp%s_base" % instance_id)
            diff_file = "%s/%s" % (temp_dir_name, "temp%s" % instance_id)
            with settings(host_string=cfg.host):
                with forward_agent(env.key_filename):
                    run(("glance --os-username=%s --os-password=%s --os-tenant-name=%s " +
                         "--os-auth-url=%s " +
                        "image-download %s > %s") %
                        (cfg.user,
                         cfg.password,
                         cfg.tenant,
                         cfg.auth_url,
                         image_id,
                         base_file))
            instance[DIFF][PATH_DST] = diff_file
            instance[DIFF][HOST_DST] = self.dst_cloud.getIpSsh()
        return {
            'info': info
        }
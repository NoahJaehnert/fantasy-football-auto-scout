from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions
from aws_cdk.core import Stack, Construct, App
import os


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        container_port = 5000
        ApplicationLoadBalancedFargateService(
            self,
            'yahoo-proxy-server',
            memory_limit_mib=1024,
            cpu=1024,
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                image=ContainerImage.from_asset(
                    os.getcwd(),
                    file='Dockerfile',
                    repository_name=_id,
                    exclude=['cdk.out'],
                    build_args={
                        'PROXY_PORT': str(container_port)
                    }
                ),
                container_port=container_port,
            ),
            listener_port=80,
            public_load_balancer=True
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'FantasyFootballAutoScout')
    app.synth()
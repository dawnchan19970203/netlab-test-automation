import time


def test_ospf_link_failure_and_recovery(
        real_r1,
        cleanup_manager,
        topology
    ):
    # 1. 故障前确认邻居正常
    output = real_r1.execute_command("show ip ospf neighbor")
    assert "FULL" in output

    r1_interface = (
    topology["links"]["r1_r2"]["r1"]["interface"]
    )

    # 2. shutdown R1 与 R2 的互联接口
    real_r1.execute_config(
        f"interface {r1_interface}",
        "shutdown"
    )

    # 3. 立刻注册恢复动作
    cleanup_manager.add(
        real_r1.execute_config,
        [
            f"interface {r1_interface}",
            "no shutdown"
        ]
    )


    output = real_r1.execute_command("show ip ospf neighbor")

    assert "FULL" not in output, (
        f"链路 shutdown 后 OSPF 邻居仍然存在：\n{output}"
    )


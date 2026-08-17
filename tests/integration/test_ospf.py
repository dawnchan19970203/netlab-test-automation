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

def test_ospf_neighbor_full(real_r1, topology):
    link = topology["links"]["r1_r2"]

    neighbor_id = topology["loopbacks"]["r2"]
    neighbor_address = link["r2"]["ip"]
    local_interface = link["r1"]["interface"]

    neighbor_output = real_r1.execute_command(
        "show ip ospf neighbor"
    )

    neighbor_line = next(
        (
            line
            for line in neighbor_output.splitlines()
            if neighbor_id in line
            and neighbor_address in line
        ),
        None,
    )

    assert neighbor_line is not None, (
        f"没有找到预期的 OSPF 邻居："
        f"neighbor_id={neighbor_id}, "
        f"address={neighbor_address}\n"
        f"实际输出：\n{neighbor_output}"
    )

    assert "FULL/" in neighbor_line, (
        f"OSPF 邻居 {neighbor_id} "
        f"没有达到 FULL 状态：\n"
        f"{neighbor_line}"
    )

    interface_output = real_r1.execute_command(
        f"show ip ospf interface {local_interface}"
    )

    assert f"{local_interface} is up" in interface_output, (
        f"OSPF 本地接口 {local_interface} 状态异常：\n"
        f"{interface_output}"
    )

    assert f"Adjacent with neighbor {neighbor_id}" in interface_output, (
        f"接口 {local_interface} "
        f"没有与邻居 {neighbor_id} 建立完整邻接：\n"
        f"{interface_output}"
    )



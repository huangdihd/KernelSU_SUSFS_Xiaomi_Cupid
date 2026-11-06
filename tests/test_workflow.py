"""Regression checks for the LOS 24 workflow (requires PyYAML)."""
import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # BaseLoader preserves GitHub's `on` key rather than YAML 1.1's boolean.
        cls.workflow = yaml.load(
            (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        cls.inputs = cls.workflow["on"]["workflow_dispatch"]["inputs"]
        cls.steps = cls.workflow["jobs"]["Kernel_CI"]["steps"]

    def step(self, name):
        return next(step for step in self.steps if step.get("name") == name)

    def test_los24_defaults(self):
        self.assertEqual(self.inputs["kernel_branch"]["default"], "lineage-24.0")
        clang = self.inputs["clang_version"]
        self.assertEqual(clang["default"], "clang-r596125")
        self.assertIn(clang["default"], clang["options"])
        self.assertIn("clang-r563880c", clang["options"])

    def test_toolchain_source_keeps_android16_support(self):
        script = self.step("Download AOSP Clang")["run"]
        self.assertIn('clang-r596125) CLANG_REF="29182889399818f97baa65ea238c80e8117981eb"', script)
        self.assertIn('*) CLANG_REF="refs/heads/android16-qpr2-release"', script)
        self.assertIn('/+archive/${CLANG_REF}/${{ inputs.clang_version }}.tar.gz', script)

    def test_cache_isolated_by_compiler(self):
        setup = self.step("Configure ccache dir and key")["run"]
        self.assertIn('CCACHE_REAL_KEY="${CCACHE_REAL_KEY}-${{ inputs.clang_version }}"', setup)
        restore = self.step("Restore ccache")["with"]
        expected_key = "${{ env.CCACHE_REAL_KEY }}-${{ runner.os }}-${{ inputs.kernel_branch }}"
        self.assertEqual(restore["key"], expected_key)
        self.assertEqual(self.step("Save ccache")["with"]["key"], expected_key)
        for key in restore["restore-keys"].splitlines():
            self.assertTrue(key.startswith("${{ env.CCACHE_REAL_KEY }}-"))
        compile_script = self.step("Compile Kernel")["run"]
        self.assertIn('CCACHE_COMPILERCHECK="content"', compile_script)
        self.assertNotIn('CCACHE_COMPILERCHECK="none"', compile_script)

    def test_existing_kernel_features_remain_available(self):
        self.assertIn("BakaSU", self.inputs["ksu_type"]["options"])
        for feature in ("susfs", "BBG", "rekernel", "droidspaces"):
            self.assertEqual(self.inputs[feature]["type"], "boolean")
        script = self.step("Compile Kernel")["run"]
        for integration in (
            "Baka-SU/BakaSU/main/kernel/setup.sh",
            "gki-android12-5.10",
            "susfs_guard_priority_helpers.py",
            "CONFIG_KSU_SUSFS=y",
            "vc-teahouse/Baseband-guard",
            "CONFIG_BBG=y",
            "Sakion-Team/Re-Kernel.git",
            "CONFIG_REKERNEL=y",
            "001.GKI-below-6.12-fix_sysvipc_kabi_6_7_8.patch",
            "002.5.10_or_lower_use_android_abi_padding_for_posix_mqueue.patch",
            'DROIDSPACES_CONFIG="vendor/droidspaces.config"',
            "vendor/debugfs.config ${DROIDSPACES_CONFIG}",
        ):
            self.assertIn(integration, script)


if __name__ == "__main__":
    unittest.main()

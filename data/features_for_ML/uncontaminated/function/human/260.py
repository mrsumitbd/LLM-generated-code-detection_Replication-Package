from pathlib import Path
from ghidra.program.model.listing import Program
from ghidra.program.flatapi import FlatProgramAPI
from ghidra.program.flatapi import FlatProgramAPI
from ghidra.program.model.listing import Program
from typing import TYPE_CHECKING, Any, Union
from ghidra.program.flatapi import FlatProgramAPI
from ghidra.util.task import ConsoleTaskMonitor
from java.io import File
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.listing import Program
from ghidra.app.script import GhidraScriptUtil
from ghidra.program.model.listing import Program
from java.io import File
from ghidra.program.util import GhidraProgramUtilities

def analyze_program(  # noqa C901
        self,
        df_or_prog: Union["DomainFile", "Program"],
        require_symbols: bool = True,
        force_analysis: bool = False,
        verbose_analysis: bool = False,
    ):
        from ghidra.app.script import GhidraScriptUtil
        from ghidra.program.flatapi import FlatProgramAPI
        from ghidra.program.model.listing import Program
        from ghidra.program.util import GhidraProgramUtilities
        from ghidra.util.task import ConsoleTaskMonitor

        if self.programs.get(df_or_prog.name):
            # program already opened and initialized
            program = self.programs[df_or_prog.name].program
        else:
            # open program from Ghidra Project
            program = self.project.openProgram("/", df_or_prog.getName(), False)
            self.programs[df_or_prog.name] = self._init_program_info(program)

        assert isinstance(program, Program)

        logger.info(f"Analyzing: {program}")

        for gdt in self.gdts:
            logger.info(f"Loading GDT: {gdt}")
            if not Path(gdt).exists():
                raise FileNotFoundError(f"GDT Path not found {gdt}")
            self.apply_gdt(program, gdt)

        gdt_names = [name for name in program.getDataTypeManager().getSourceArchives()]
        if len(gdt_names) > 0:
            logger.debug(f"Using file gdts: {gdt_names}")

        try:
            if verbose_analysis or self.verbose_analysis:
                monitor = ConsoleTaskMonitor()
                flat_api = FlatProgramAPI(program, monitor)
            else:
                flat_api = FlatProgramAPI(program)

            if (
                GhidraProgramUtilities.shouldAskToAnalyze(program)
                or force_analysis
                or self.force_analysis
            ):
                GhidraScriptUtil.acquireBundleHostReference()

                if program and program.getFunctionManager().getFunctionCount() > 1000:
                    # Force Decomp Param ID is not set
                    if (
                        self.program_options is not None
                        and self.program_options.get("program_options", {})
                        .get("Analyzers", {})
                        .get("Decompiler Parameter ID")
                        is None
                    ):
                        self.set_analysis_option(program, "Decompiler Parameter ID", True)

                if self.program_options:
                    analyzer_options = self.program_options.get("program_options", {}).get(
                        "Analyzers", {}
                    )
                    for k, v in analyzer_options.items():
                        logger.info(f"Setting prog option:{k} with value:{v}")
                        self.set_analysis_option(program, k, v)

                if self.no_symbols:
                    logger.warn(
                        f"Disabling symbols for analysis! --no-symbols flag: {self.no_symbols}"
                    )
                    self.set_analysis_option(program, "PDB Universal", False)

                logger.info(f"Starting Ghidra analysis of {program}...")
                try:
                    flat_api.analyzeAll(program)
                    if hasattr(GhidraProgramUtilities, "setAnalyzedFlag"):
                        GhidraProgramUtilities.setAnalyzedFlag(program, True)
                    elif hasattr(GhidraProgramUtilities, "markProgramAnalyzed"):
                        GhidraProgramUtilities.markProgramAnalyzed(program)
                    else:
                        raise Exception("Missing set analyzed flag method!")
                finally:
                    GhidraScriptUtil.releaseBundleHostReference()
                    self.project.save(program)
            else:
                logger.info(f"Analysis already complete.. skipping {program}!")
        finally:
            if self.gzfs_path is not None:
                from java.io import File  # type: ignore

                gzf_file = self.gzfs_path / f"{program.getDomainFile().getName()}.gzf"
                self.project.saveAsPackedFile(program, File(str(gzf_file.absolute())), True)

        logger.info(f"Analysis for {df_or_prog.getName()} complete")
        self.programs[df_or_prog.name].ghidra_analysis_complete = True
        return df_or_prog
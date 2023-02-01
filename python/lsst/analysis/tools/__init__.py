# This file is part of analysis_tools.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
r"""This packages contains various analysis tools and PipelineTasks which
run them.

There are two types of primary tools within this package; `AnalysisMetrics
and `AnalysisPlots`, both of which are specialized subclasses of `AnalysisTool`.

`AnalysisTool`\ s are objects that have three stages; prep, process, and
post-process. Creating a new `AnalysisTool` is the process of choosing (though
configuration) what `AnalysisAction` will run for each of those stages.

`AnalysisTool`\ s and `AnalysisAction`\ s are subclasses of
`~lsst.pex.config.configurableActions.ConfigurableAction`\ s. These objects are
special types that are configured _prior_ to any code execution, and behave as
functions at runtime. The configuration state of a
`~lsst.pex.config.configurableActions.ConfigurableAction` is saved separately
from the object itself, which allows
"""

from .interfaces import *
from .statistics import *
from .version import *  # Generated by sconsUtils

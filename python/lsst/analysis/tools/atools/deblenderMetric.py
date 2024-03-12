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
from __future__ import annotations

__all__ = ("ParentDeblenderMetrics", "SkippedDeblenderMetrics", "BlendMetrics", "IsolatedDeblenderMetrics")

from ..actions.scalar.scalarActions import CountAction, MeanAction, SumAction
from ..actions.vector.selectors import (
    ChildObjectSelector,
    FlagSelector,
    ParentObjectSelector,
    ThresholdSelector,
)
from ..interfaces import AnalysisTool


class ParentDeblenderMetrics(AnalysisTool):
    """Calculate metrics based on the performance of the deblender"""

    def setDefaults(self):
        super().setDefaults()

        # Only select parents
        self.prep.selectors.parentSelector = ParentObjectSelector()

        # Statistics for parent blends
        self.process.calculateActions.numParents = CountAction(vectorKey="parentObjectId")
        self.process.calculateActions.numDeblendFailed = SumAction(vectorKey="deblend_failed")
        self.process.calculateActions.numIncompleteData = SumAction(vectorKey="deblend_incompleteData")

        # Total number of detected peaks
        self.process.calculateActions.numDetectedPeaks = SumAction(vectorKey="deblend_nPeaks")
        # Total number of deblended children
        self.process.calculateActions.numDeblendedChildren = SumAction(vectorKey="deblend_nChild")

        self.produce.metric.units = {
            "numParents": "",
            "numDeblendFailed": "",
            "numIncompleteData": "",
            "numDetectedPeaks": "",
            "numDeblendedChildren": "",
        }


class SkippedDeblenderMetrics(AnalysisTool):
    """Calculate metrics based on blends skipped by the deblender"""

    def setDefaults(self):
        super().setDefaults()

        # Only select non-sky object parents that were skipped but did not fail
        # This also excludes isolated objects that were skipped
        # if isolated objects are not being deblended
        self.prep.selectors.parentSelector = ParentObjectSelector()
        self.prep.selectors.skippedSelector = FlagSelector()
        self.prep.selectors.skippedSelector.selectWhenTrue = ["deblend_skipped"]
        self.prep.selectors.skippedSelector.selectWhenFalse = ["deblend_failed", "deblend_isolatedParent"]

        # Statistics for skipped blends
        self.process.calculateActions.numSkippedBlends = CountAction(vectorKey="parentObjectId")
        self.process.calculateActions.numBlendParentTooBig = SumAction(vectorKey="deblend_parentTooBig")
        self.process.calculateActions.numBlendTooManyPeaks = SumAction(vectorKey="deblend_tooManyPeaks")
        self.process.calculateActions.numBlendTooManyMasked = SumAction(vectorKey="deblend_masked")

        # Total number of skipped peaks
        self.process.calculateActions.numSkippedPeaks = SumAction(vectorKey="deblend_nPeaks")

        self.produce.metric.units = {
            "numSkippedBlends": "",
            "numBlendParentTooBig": "",
            "numBlendTooManyPeaks": "",
            "numBlendTooManyMasked": "",
            "numSkippedPeaks": "",
        }


class BlendMetrics(AnalysisTool):
    """Calculate metrics based on the performance of the deblender for blends
    with multiple children
    """

    def setDefaults(self):
        super().setDefaults()

        # Only select parents that were successfully deblended
        # with more than one child
        self.prep.selectors.parentSelector = ParentObjectSelector()
        self.prep.selectors.blendSelector = ThresholdSelector()
        self.prep.selectors.blendSelector.vectorKey = "deblend_nChild"
        self.prep.selectors.blendSelector.op = "gt"
        self.prep.selectors.blendSelector.threshold = 1

        # Statistics for blended parents
        self.process.calculateActions.numBlends = CountAction(vectorKey="parentObjectId")
        self.process.calculateActions.meanBlendIterations = MeanAction(vectorKey="deblend_iterations")
        self.process.calculateActions.meanBlendLogL = MeanAction(vectorKey="deblend_logL")

        self.produce.metric.units = {
            "numBlends": "",
            "meanBlendIterations": "",
            "meanBlendLogL": "",
        }


class IsolatedDeblenderMetrics(AnalysisTool):
    """Calculate metrics based on the performance of the deblender for
    parents with only a single child peak.
    """

    def setDefaults(self):
        super().setDefaults()

        # Only select parents that were successfully deblended with one child
        self.prep.selectors.parentSelector = ParentObjectSelector()
        self.prep.selectors.blendSelector = ThresholdSelector()
        self.prep.selectors.blendSelector.vectorKey = "deblend_nChild"
        self.prep.selectors.blendSelector.op = "eq"
        self.prep.selectors.blendSelector.threshold = 1

        # Statistics for isolated parent scarlet_lite models
        self.process.calculateActions.numIsolated = CountAction(vectorKey="parentObjectId")
        self.process.calculateActions.meanIsolatedIterations = MeanAction(vectorKey="deblend_iterations")
        self.process.calculateActions.meanIsolatedLogL = MeanAction(vectorKey="deblend_logL")

        self.produce.metric.units = {
            "numIsolated": "",
            "meanIsolatedIterations": "",
            "meanIsolatedLogL": "",
        }


class ChildDeblenderMetrics(AnalysisTool):
    """Calculate metrics based on the performance of the deblender for
    single sources.
    """

    def setDefaults(self):
        super().setDefaults()
        self.prep.selectors.childSelector = ChildObjectSelector()
        self.process.calculateActions.zeroFlux = SumAction(vectorKey="deblend_zeroFlux")

        self.produce.metric.units = {
            "zeroFlux": "",
        }

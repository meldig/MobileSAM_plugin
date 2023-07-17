import os

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterFeatureSource)
from qgis import processing
from mobile_sam import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import numpy as np
import supervision as sv
import cv2 as cv


class MobileSamAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    IMG_REF = 'IMG_REF'
    INPUT_LAYER = 'INPUT_LAYER'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return MobileSamAlgorithm()

    def name(self):
        return 'mobilesam'

    def displayName(self):
        return self.tr('Mobile SAM')

    def group(self):
        return None

    def groupId(self):
        return None

    def shortHelpString(self):
        return self.tr("Mobile SAM est un outil permettant de segmenter des images automatiquement.")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.IMG_REF,
                self.tr('The reference image'),
                optional=False
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr('The points or boxes layer'),
                optional=False
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        def get_inputfilepath(layer):
            return os.path.realpath(layer.source().split("|layername")[0])

        img_ref = get_inputfilepath(self.parameterAsRasterLayer(parameters, self.IMG_REF, context))
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)

        image_array = cv.imread(img_ref)

        scores_array = []

        model_type = "vit_t"
        sam_checkpoint = "D:\\calba\\mobilesam_plugin\\weights\\mobile_sam.pt"

        m_sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        m_sam.eval()

        for feature in input_layer.getFeatures():
            prompts = []
            prompts_types = []

            geometry = feature.geometry()
            point = geometry.pointOnSurface().asPoint()

            prompts.append([point.x(), point.y()])
            prompts_types.append(1)

            prompts = np.asarray(prompts)
            prompts_types = np.asarray(prompts_types)

            predictor = SamPredictor(m_sam)
            predictor.set_image(image_array)
            masks, scores, _ = predictor.predict(prompts, prompts_types)
            scores_array.append(scores)

        return {self.OUTPUT: scores_array}
